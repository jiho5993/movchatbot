FROM python:3.8

RUN mkdir /django
WORKDIR /django

ADD requirements.txt /django/

RUN apt-get update && apt-get -y install \
    libpq-dev
RUN apt-get install -y netcat
RUN python -m pip install --upgrade pip
RUN pip install -r requirements.txt
RUN pip install gunicorn

ADD . /django/

EXPOSE 3000

CMD ["python3", "manage.py", "runserver", "0:3000"]