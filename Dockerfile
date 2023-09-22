FROM python:3.10

ENV PYTHONUNBUFFERED True
ENV PIPENV_VENV_IN_PROJECT 1

ENV APP_HOME /app
WORKDIR $APP_HOME
COPY . ./

RUN pip install pipenv
RUN pipenv install

# As an example here we're running the web service with one worker on uvicorn.
CMD pipenv run uvicorn src.main:app --host 0.0.0.0 --port ${PORT} --workers 1
