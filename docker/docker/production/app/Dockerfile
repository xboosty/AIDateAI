FROM python:3.9.18-bullseye

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

ARG APP_HOME=/app

# Install required system dependencies
RUN apt-get update && apt-get install --no-install-recommends -y \
  ffmpeg \
  && apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false \
  && rm -rf /var/lib/apt/lists/*

COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt

COPY ai_requirements.txt ai_requirements.txt

RUN pip install -r ai_requirements.txt

#RUN pip install "git+https://github.com/openai/whisper.git" 

COPY ./docker/development/app/start /start
RUN sed -i 's/\r$//g' /start
RUN chmod +x /start

COPY ./fastapi_enterview $APP_HOME

WORKDIR $APP_HOME

EXPOSE 80
