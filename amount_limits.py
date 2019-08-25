import datetime as dt
from enviroment import AMOUNT_LIMITS_CONFIG
import ast

amounts_limits_config = ast.literal_eval(AMOUNT_LIMITS_CONFIG)
assert type(amounts_limits_config) is dict


list_request_amount = []
check_datatime = dt.datetime.now()
list_deltatime_request = []


def get_deltadatetime(request):
    global check_datatime
    if check_datatime == dt.datetime.now():
        deltadatetime = 0
        return deltadatetime
    else:
        deltadatetime = (request['datetime'] - check_datatime).seconds
        check_datatime = request['datetime']
        return deltadatetime


def get_check_amount_limit(request):
    global list_deltatime_request
    global list_request_amount
    deltatime = get_deltadatetime(request)
    list_deltatime_request.append(deltatime)
    amount = request['amount']
    sum_amount = sum(list_request_amount)
    for key, value in amounts_limits_config.items():
        if sum(list_deltatime_request) <= key:
            list_request_amount.append(amount)
            if sum_amount <= value:
                check_request_result_ok = "OK"
                print(key, value)
                return check_request_result_ok
            else:
                result = "amount limit exeeded ({}/{}sec)".format(value, key)
                return result
    result = "amount limit exeeded ({}/{}sec)".format(value, key)
    list_request_amount = []
    list_deltatime_request = []
    return result