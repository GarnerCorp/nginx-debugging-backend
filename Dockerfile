FROM python:3.6-slim

WORKDIR /app

COPY requirements.txt /app/requirements.txt
COPY debug.py /app
RUN pip install -r requirements.txt --src /usr/local/src

EXPOSE 8080:8080
CMD [ "/app/debug.py" ]
