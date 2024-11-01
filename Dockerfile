FROM python:3.10-alpine

WORKDIR /app

COPY ./requirements.txt .
COPY ./entrypoint.sh .

RUN apk add --no-cache mysql-client

RUN pip install --upgrade pip
RUN pip install --upgrade pip setuptools wheel
RUN pip install --no-cache-dir -r requirements.txt

RUN pip install -r requirements.txt
ENV PYTHONPATH .

COPY . .

EXPOSE 5000

ENTRYPOINT ["sh", "/app/entrypoint.sh"]