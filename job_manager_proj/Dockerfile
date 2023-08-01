FROM python:3.9-slim
MAINTAINER Alex Maximchik 'alex@mail.ru'

SHELL ["/bin/bash", "-c"]

# set the environment variables
ENV PYTHONFAULTHANDLER=1 \
  PYTHONUNBUFFERED=1 \
  PYTHONHASHSEED=random \
  PIP_NO_CACHE_DIR=off \
  PIP_DISABLE_PIP_VERSION_CHECK=on \
  PIP_DEFAULT_TIMEOUT=100 \
  POETRY_VERSION=1.3.2


RUN pip install --upgrade pip
RUN pip install "poetry==$POETRY_VERSION"
RUN useradd -rms /bin/bash job_manager && chmod 777 /opt /run

# mkdir + cd
WORKDIR /app

RUN chown -R job_manager:job_manager /app && chmod 755 /app

COPY --chown=job_manager . .
RUN poetry config virtualenvs.create false && poetry config installer.max-workers 10 \
&& poetry install --no-root