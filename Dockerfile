FROM python:3.7-alpine

RUN apk update
RUN apk upgrade
RUN apk add curl

WORKDIR /app
COPY . .

ENV FLASK_APP=app.py
ENV PYTHONPATH=/app

RUN if [ "$FLASK_ENV" = "development" ]; then pip install -r requirements/dev.txt; else pip install -r requirements/prod.txt; fi

EXPOSE 8888

CMD ["flask", "run", "--host 0.0.0.0", "--port 8888"]