FROM python:3.12-bookworm

RUN pip install poetry

COPY . .

RUN poetry install

EXPOSE 80

ENTRYPOINT ["poetry", "run", "uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "80"]
