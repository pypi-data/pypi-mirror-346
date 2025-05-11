FROM python:3.11-buster

RUN pip install uvicorn
RUN pip install persona-toolkit

ENV POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_IN_PROJECT=1 \
    POETRY_VIRTUALENVS_CREATE=1 \
    POETRY_CACHE_DIR=/tmp/poetry_cache

ENV PORT=8000

WORKDIR /app

COPY docker/run.sh ./
COPY tools ./tools
RUN chmod +x ./run.sh

ENTRYPOINT ["./run.sh"]

