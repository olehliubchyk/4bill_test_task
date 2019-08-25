FROM python:3.6

ADD . /4bill_test_task
WORKDIR /4bill_test_task

ENV TZ=Europe/Kiev
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

RUN pip3 install -r requirements.txt
CMD python3 main.py