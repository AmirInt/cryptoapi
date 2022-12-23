FROM python:3.8.0-alpine

WORKDIR .

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

CMD python app.py