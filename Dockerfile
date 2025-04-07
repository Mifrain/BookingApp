FROM python:3.12

RUN mkdir /booking

WORKDIR /booking

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

RUN chmod a+x /booking/docker/*.sh

CMD ["gunicorn", "app.main:app", "--workers", "4", "--worker-class", "uvicorn.workers.Uvicornworker", "--bind=0.0.0.0:8000"]