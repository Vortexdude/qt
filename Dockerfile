FROM python:3.10-bullseye AS base
RUN apt-get update \
    && apt-get upgrade -y \
    && apt-get install -y --no-install-recommends curl git build-essential \
    && apt-get autoremove -y
ENV POETRY_HOME="/opt/poetry"    
RUN curl -sSL https://install.python-poetry.org | python3 -

FROM base AS install
LABEL maintainer="Nitin Namdev"
WORKDIR /home/code

# allow controlling the poetry installation of dependencies via external args
ARG INSTALL_ARGS="--no-root --only main"
ENV POETRY_HOME="/opt/poetry"
ENV PATH="$POETRY_HOME/bin:$PATH"
COPY pyproject.toml poetry.lock ./

RUN poetry config virtualenvs.create false \
    && poetry install ${INSTALL_ARGS}


# Cleanup
RUN curl -sSL https://install.python-poetry.org | python3 - --uninstall
RUN apt-get purge -y curl git build-essential \
    && apt-get clean -y \
    && rm -rf /root/.cache \
    && rm -rf /var/apt/lists/* \
    && rm -rf /var/cache/apt/*

FROM install AS app-image

COPY . /home/code/

RUN addgroup --system --gid 1001 "python"
RUN adduser --system --uid 1001 "python"
USER "python"

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080", "--reload"]
