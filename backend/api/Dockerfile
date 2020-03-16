FROM python:3.6.10-alpine

WORKDIR /usr/src/stump_backend/api

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# psycopg2 dependencies
RUN apk update \
  && apk add postgresql-dev gcc python3-dev musl-dev

# install python dependencies
COPY ./Pipfile .
RUN pip install --upgrade pip \
  && pip install pipenv \
  && pipenv lock -r > ./requirements.txt \
  && pipenv lock -r --dev >> ./requirements.txt \
  && pip install -r requirements.txt

# copy Django source code
COPY . .

# must run manage.py runserver from top level python module
WORKDIR stump_backend

EXPOSE 8000

ENTRYPOINT ["/usr/src/stump_backend/api/stump_backend/entrypoint.sh"]
