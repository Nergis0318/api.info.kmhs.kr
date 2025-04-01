FROM python:alpine

COPY . .

RUN pip install poetry && poetry install

EXPOSE 8000
CMD poetry run fastapi run
