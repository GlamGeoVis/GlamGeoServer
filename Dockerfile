FROM python:3.6

WORKDIR /app

COPY requirements.txt /app/
RUN pip3 install -r requirements.txt

RUN pip3 install gunicorn==19.7.1

COPY . /app

STOPSIGNAL SIGINT

CMD gunicorn --preload --workers 3 --max-requests 10 --timeout 15 --bind 0.0.0.0:8001 --access-logfile - --error-logfile - server:app

EXPOSE 8001