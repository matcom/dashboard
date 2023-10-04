FROM python:3.10

WORKDIR /src

COPY requirements.txt /src/requirements.txt
COPY makefile /src/makefile

RUN --mount=type=cache,target=/root/.cache/pip make install
