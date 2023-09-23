FROM python:3.11
LABEL authors="palibrix"

WORKDIR /task
COPY ./requirements.txt /task/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /task/requirements.txt

COPY ./app /task/app