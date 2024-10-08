FROM ghcr.io/astral-sh/uv:python3.12-bookworm-slim AS builder

ARG APP_HOME=/usr/src/app
WORKDIR ${APP_HOME}

ENV PYTHONDONTWRITEBYTECODE 1 \
  PYTHONUNBUFFERED 1 \
  UV_COMPILE_BYTECODE=1 \
  UV_LINK_MODE=copy

RUN apt update \
  && apt install -y --no-install-recommends curl git libpq-dev gcc libglu1 \
  && pip install --no-cache-dir --upgrade pip \
  && pip install --no-cache-dir psycopg psycopg-binary \
  && apt purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false \
  && rm -rf /var/lib/apt/lists/*

# Install dependencies
RUN --mount=type=cache,target=/root/.cache/uv \
  --mount=type=bind,source=uv.lock,target=uv.lock \
  --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
  uv sync --frozen --no-install-project

ADD . ${APP_HOME}

RUN --mount=type=cache,target=/root/.cache/uv \
  uv sync --frozen --no-dev


# Use a final image without uv
FROM python:3.13-slim-bookworm

# Copy the application from the builder
COPY --from=builder --chown=app:app ${APP_HOME} ${APP_HOME}

# Place executables in the environment at the front of the path
ENV PATH="/usr/src/app/.venv/bin:$PATH"

COPY ./docker/django/entrypoint ${APP_HOME}/docker/django/entrypoint
COPY ./docker/django/start_dev ${APP_HOME}/docker/django/start_dev

RUN chmod +x ${APP_HOME}/docker/django/start_dev ${APP_HOME}/docker/django/entrypoint \
  && sed -i 's/\r$//g' ${APP_HOME}/docker/django/start_dev ${APP_HOME}/docker/django/entrypoint

ENTRYPOINT ["/usr/src/app/docker/django/entrypoint"]
