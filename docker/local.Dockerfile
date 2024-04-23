FROM python:3.11.2-slim

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1
RUN apt-get update \
# dependencies for building Python packages
&& apt-get install -y build-essential \
# psycopg2 dependencies
&& apt-get install -y libpq-dev \
# Additional dependencies
&& apt-get install -y telnet netcat \
# cleaning up unused files
&& apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false \
&& rm -rf /var/lib/apt/lists/*
# Installing all python dependencies
RUN pip install --upgrade pip
ADD requirements/ requirements/
RUN pip install -r requirements/base.txt

# Get the django project into the docker container
RUN mkdir /app
WORKDIR /app
ADD ./ /app/
