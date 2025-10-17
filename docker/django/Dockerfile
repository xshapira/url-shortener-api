FROM python:3.14-slim-bookworm AS builder

ARG APP_HOME=/usr/src/app
WORKDIR ${APP_HOME}

ENV PYTHONDONTWRITEBYTECODE 1 \
  PYTHONUNBUFFERED 1 \
  UV_COMPILE_BYTECODE=1 \
  UV_LINK_MODE=copy \
  UV_PROJECT_ENVIRONMENT=/usr/src/app/.venv

RUN apt update \
  && apt install -y --no-install-recommends curl git libpq-dev gcc libglu1 \
  && pip install --no-cache-dir --upgrade pip \
  && pip install --no-cache-dir psycopg psycopg-binary \
  && apt purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false \
  && rm -rf /var/lib/apt/lists/*

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Install dependencies
RUN --mount=type=cache,target=/root/.cache/uv \
  --mount=type=bind,source=uv.lock,target=uv.lock \
  --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
  uv sync --frozen --no-install-project --no-editable

COPY uv.lock pyproject.toml ./

ADD . ${APP_HOME}

RUN --mount=type=cache,target=/root/.cache/uv \
  uv sync --frozen --no-editable

# Place executables in the environment at the front of the path
ENV PATH="/usr/src/app/.venv/bin:$PATH"

COPY ./docker/django/entrypoint ${APP_HOME}/docker/django/entrypoint
COPY ./docker/django/start_dev ${APP_HOME}/docker/django/start_dev

RUN chmod +x ${APP_HOME}/docker/django/start_dev ${APP_HOME}/docker/django/entrypoint \
  && sed -i 's/\r$//g' ${APP_HOME}/docker/django/start_dev ${APP_HOME}/docker/django/entrypoint

ENTRYPOINT ["/usr/src/app/docker/django/entrypoint"]
