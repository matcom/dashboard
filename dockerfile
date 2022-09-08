FROM python:3.8

WORKDIR /src

COPY requirements.txt /src/requirements.txt
COPY makefile /src/makefile

RUN make install
