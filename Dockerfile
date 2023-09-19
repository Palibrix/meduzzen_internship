FROM python:3.11
LABEL authors="palibrix"

WORKDIR /task
COPY ./requirements.txt /task/requirements.txt
COPY ./requirements_dev.txt /task/requirements_dev.txt

RUN pip install --no-cache-dir --upgrade -r /task/requirements_dev.txt

COPY ./app /task/app

