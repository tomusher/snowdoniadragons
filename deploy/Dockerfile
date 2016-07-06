FROM python:3.5
ENV PYTHONUNBUFFERED 1

RUN mkdir /usr/src/app
WORKDIR /usr/src/app

ADD deploy/uwsgi.ini /usr/src/
RUN pip install uwsgi
ADD app/requirements.txt /usr/src/app/
RUN pip install -r requirements.txt
ADD app/ /usr/src/app/

CMD uwsgi --ini ../uwsgi.ini
