#FROM python:3.7.2-alpine
FROM kennethreitz/pipenv

WORKDIR /backapp

ADD . /backapp

#RUN pip install pipenv
RUN pipenv install --system

EXPOSE 80

ENV SOMEENV somevalue

CMD python3 -m unittest -v flightservice.test_xcontest
