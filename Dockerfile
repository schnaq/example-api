FROM python:3.12-bookworm

RUN pip install poetry

COPY . .

RUN poetry install

EXPOSE 80

ENTRYPOINT ["poetry", "run", "main.py"]
