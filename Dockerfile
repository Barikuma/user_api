FROM python:latest

WORKDIR /app

COPY my_api.py .
COPY requirements.txt .
COPY users.json .

RUN pip3 install -r requirements.txt

EXPOSE 8000

CMD ["python3", "my_api.py"]
