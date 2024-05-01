FROM python:3.8-slim

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . .

CMD [ "gunicorn", "-w", "4", "-b", "0.0.0.0", "--threads=3", "--worker-connections=1000", "app:app"]
EXPOSE 8000