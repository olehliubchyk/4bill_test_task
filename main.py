import datetime as dt
from enviroment import FLASK_HOST, FLASK_PORT, DATABASE_URL
from flask import Flask, make_response
from custom_exceptions import NotFoundException
import json
from amount_limits import get_check_amount_limit
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class AmountRequest(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    datetime_request = db.Column(db.DateTime)
    amount_request = db.Column(db.Integer)

    def __init__(self, datetime, amount_request):
        self.datetime_request = datetime
        self.amount_request = amount_request


db.create_all()


def save_request_to_db(amount_request):
    datetime = amount_request['datetime']
    amount_request = amount_request['amount']

    db.session.add(AmountRequest(datetime, amount_request))
    db.session.commit()


@app.route('/request/<int:amount>')
def check_amount_limit(amount):
    try:
        amount_request = {'datetime': dt.datetime.now(), 'amount': amount}
        result_checked = get_check_amount_limit(amount_request)
        save_request_to_db(amount_request)
        if result_checked == "OK":
            return make_response(json.dumps(
                {
                    "result": "OK"
                }
                ), 200)
        else:
            return make_response(json.dumps(
                {
                     "error": result_checked
                }
                ), 429)
    except NotFoundException:
        return make_response(json.dumps({"Error": "HTTP 404 Not Found"}), 404)
    except Exception:
        return make_response(json.dumps({"Error": "HTTP 500 Internal Server Error"}), 500)


if __name__ == "__main__":
    app.run(host=FLASK_HOST, port=FLASK_PORT, debug=True)