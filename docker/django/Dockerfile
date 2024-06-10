FROM python:3.12-slim-bookworm AS base

ARG APP_HOME=/usr/src/app
WORKDIR ${APP_HOME}

ARG POETRY_HOME=/usr/local/poetry

ENV PYTHONDONTWRITEBYTECODE 1 \
  PYTHONUNBUFFERED 1 \
  POETRY_HOME=${POETRY_HOME} \
  PYTHONPATH=${PYTHONPATH}:${PWD}

ENV PATH="$POETRY_HOME/bin:$PATH"

RUN apt update \
  && apt install -y --no-install-recommends curl git libpq-dev gcc libglu1 \
  && pip install --no-cache-dir --upgrade pip \
  && pip install --no-cache-dir psycopg psycopg-binary \
  && curl -sSL https://install.python-poetry.org | POETRY_HOME=/usr/local/poetry python3 - \
  && apt purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false \
  && rm -rf /var/lib/apt/lists/*

COPY ./pyproject.toml ${APP_HOME}/

RUN poetry config virtualenvs.create false \
  && poetry install --no-root --no-interaction --no-ansi

FROM base AS final

COPY ./docker/django/entrypoint /usr/src/app/docker/django/entrypoint
COPY ./docker/django/start_dev /usr/src/app/docker/django/start_dev

RUN chmod +x /usr/src/app/docker/django/start_dev \
  && sed -i 's/\r$//g' /usr/src/app/docker/django/start_dev

COPY . ${APP_HOME}/

RUN chmod +x /usr/src/app/docker/django/entrypoint

ENTRYPOINT ["/usr/src/app/docker/django/entrypoint"]
