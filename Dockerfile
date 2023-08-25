FROM python:3.9.16-alpine3.16

RUN addgroup app && adduser -S -G app app

USER app

ENV PIP_DISABLE_PIP_VERSION_CHECK 1
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

COPY requirements.txt requirements.txt

RUN pip3 install --no-cache-dir --upgrade -r requirements.txt

EXPOSE 8001

COPY . .


# CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]

CMD ["gunicorn", "main:app", "--workers", "4", "--worker-class", "uvicorn.workers.UvicornWorker", "--bind", "0.0.0.0:80"]