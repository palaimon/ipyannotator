FROM ubuntu:20.04

RUN rm /bin/sh && ln -s /bin/bash /bin/sh

# See http://bugs.python.org/issue19846
ENV LANG=C.UTF-8

# build hangs on tzdata input
ENV TZ=Europe/Berlin
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

ARG MASTER_TOKEN
ENV MASTER_TOKEN=$MASTER_TOKEN

ARG STORAGE_HOST
ENV STORAGE_HOST=$STORAGE_HOST
ARG BUCKET_NAME
ENV BUCKET_NAME=$BUCKET_NAME
ARG STORAGE_REMOTE
ENV STORAGE_REMOTE=$STORAGE_REMOTE
ARG AWS_ACCESS_KEY_ID
ENV AWS_ACCESS_KEY_ID=$AWS_ACCESS_KEY_ID
ARG AWS_SECRET_ACCESS_KEY
ENV AWS_SECRET_ACCESS_KEY=$AWS_SECRET_ACCESS_KEY

RUN apt-get update && apt-get install -y --no-install-recommends \
    wget curl                                                    \
    git                                                          \
    python3-dev                                                  \
    python3-pip                                                  \
    build-essential                                              \
    libffi-dev                                                   \
    libssl-dev                                                   \
    libbz2-dev                                                   \
    libreadline-dev                                              \
    libsqlite3-dev                                               \
    netbase                                                      \
	make                                                         \
	build-essential                                              \
	ruby                                                         \
	ruby-dev                                                     \
    ca-certificates                                            &&\
    rm -rf /var/lib/apt/lists/*

ENV PYENV_ROOT=$HOME/.pyenv
ENV PATH=$PYENV_ROOT/shims:$PYENV_ROOT/bin:$PATH

RUN git clone git://github.com/yyuu/pyenv.git .pyenv

RUN pyenv install 3.8.5 -f && pyenv global 3.8.5

RUN pip install --upgrade pip

# Poetry publish command has some bugs in handling config and env variables:
# https://github.com/python-poetry/poetry/issues/2210
# https://github.com/python-poetry/poetry/issues/858
# _URL ending for repositories environment variable
# and NO /simple/ or /legacy/ etc. endpoint for real url is a must
ENV POETRY_VERSION=1.1.0             \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    POETRY_NO_INTERACTION=1          \
    POETRY_VIRTUALENVS_CREATE=false  \
    PYTHONUNBUFFERED=1               \
    POETRY_HOME=/poetry              \
    POETRY_REPOSITORIES_PALAIMON_URL=https://pypi.palaimon.io/

# uses $POETRY_VERSION & $POETRY_HOME internally
RUN curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python
ENV PATH=${POETRY_HOME}/bin:${PATH}

RUN wget -c https://downloads.kitenet.net/git-annex/linux/current/git-annex-standalone-amd64.tar.gz && \
    tar -xzf  git-annex-standalone-amd64.tar.gz

ENV PATH=/git-annex.linux:$PATH

# docker build os might not be compatible with git-annex binary
#RUN git-annex version

WORKDIR /app
COPY poetry.lock pyproject.toml /app/

RUN poetry install --no-root

COPY . /app

RUN poetry install

