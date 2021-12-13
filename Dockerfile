FROM jupyter/base-notebook

USER root

RUN apt-get update
RUN apt-get install -y libpq-dev python3-dev gcc

# Installs in conda base env
COPY ./requirements.txt .
RUN pip install -r requirements.txt
RUN playwright install; playwright install-deps
RUN rm -rf work requirements.txt
RUN mkdir app