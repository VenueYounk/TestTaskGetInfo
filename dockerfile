FROM python:3.8

WORKDIR /app

COPY ./requirements.txt /app/requirements.txt
COPY ./.env /app/.env

RUN pip install --no-cache-dir -r requirements.txt

RUN set -a && . /app/.env && set +a

COPY ./src /app/src

CMD ["python", "src/main.py"]
