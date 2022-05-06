FROM python:3.8-buster

RUN mkdir /django
WORKDIR /django

ADD requirements.txt /django/

RUN apt-get update && apt-get -y install \
    libpq-dev
RUN python -m pip install --upgrade pip
RUN pip install -r requirements.txt

ADD . /django/

ENV DEBUG_MODE=False

EXPOSE 3000

CMD ["python3", "manage.py", "runserver", "0:3000"]