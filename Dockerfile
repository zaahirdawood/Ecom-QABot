FROM python:3.11-slim

# RUN apt-get update && apt-get install -y libpq-dev

WORKDIR /src

COPY ./data/chunked_data.csv /src/data/chunked_data.csv 

COPY ["pyproject.toml","poetry.lock","./"]

RUN pip install poetry && \
    poetry config virtualenvs.create false && \
    poetry install --no-interaction --no-ansi

RUN poetry install

COPY /src/ecom_bot .

CMD ["python","app.py"]

EXPOSE 5001

ENTRYPOINT ["gunicorn", "--bind", "0.0.0.0:5000", "app:app"]