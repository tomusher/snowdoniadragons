from python:3.5
ENV PYTHONUNBUFFERED 1
RUN mkdir /usr/src/app
WORKDIR /usr/src/app
ADD app/requirements.txt /usr/src/app/
RUN pip install -r requirements.txt
ADD app/ /usr/src/app/
