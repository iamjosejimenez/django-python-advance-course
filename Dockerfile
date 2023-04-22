FROM python:3.11-alpine3.17

ENV DEV=false \
  PYTHONFAULTHANDLER=1 \
  PYTHONUNBUFFERED=1 \
  PYTHONHASHSEED=random \
  PIP_NO_CACHE_DIR=off \
  PIP_DISABLE_PIP_VERSION_CHECK=on \
  PIP_DEFAULT_TIMEOUT=100 \
  POETRY_VERSION=1.4.2

RUN pip install --upgrade pip
RUN pip install "poetry==$POETRY_VERSION"

WORKDIR /src
COPY poetry.lock pyproject.toml /src/
EXPOSE 8000

RUN apk add --update --no-cache postgresql-client && \
    apk add --update --no-cache --virtual .tmp-build-deps \
      build-base postgresql-dev musl-dev && \
    poetry config virtualenvs.create false \
      && poetry install $(test "$DEV" == true && echo "--without-dev") --no-interaction --no-ansi && \
      apk del .tmp-build-deps

COPY . /src/


