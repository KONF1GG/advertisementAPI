FROM python:3.11.8-slim-bookworm
RUN apt-get update && apt-get install -y libpq-dev gcc python3-dev --no-install-recommends


COPY /req.txt /req.txt
RUN pip install -r /req.txt

COPY /app /app
WORKDIR /app

ENV PYTHONUNBUFFERED 1

ENTRYPOINT [ "uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8080" ]
