FROM python:3.11.2

WORKDIR /intership-backend

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY ./app ./app

COPY ./migrations ./migrations

COPY alembic.ini .

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]