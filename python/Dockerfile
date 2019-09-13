FROM python:3.7
#FROM kennethreitz/pipenv

WORKDIR /backapp

ADD . /backapp

RUN pip3 install pipenv
RUN pipenv install --system --deploy


CMD python3 -m unittest -v flightservice.test_xcontest
