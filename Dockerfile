# 
FROM python:3.11-slim

# 
WORKDIR /code

# 
COPY ./requirements.txt /code/requirements.txt

# 
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

# 
COPY . .

RUN alembic upgrade head

EXPOSE 8001

# 
CMD ["gunicorn", "main:app", "--bind", ":8001",  "--worker-class", "uvicorn.workers.UvicornWorker" ]
