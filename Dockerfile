FROM python:3.12-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

COPY . /app

EXPOSE 10000

CMD sh -lc 'python3 run.py --serve --host 0.0.0.0 --port "${PORT:-10000}" --no-reload'
