FROM ubuntu:20.04

RUN rm /bin/sh && ln -s /bin/bash /bin/sh

# See http://bugs.python.org/issue19846
ENV LANG=C.UTF-8

# build hangs on tzdata input
ENV TZ=Europe/Berlin
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

ENV POETRY_VERSION=1.1.0             \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    POETRY_NO_INTERACTION=1          \
    POETRY_VIRTUALENVS_CREATE=false  \
    PYTHONUNBUFFERED=1               \
    POETRY_HOME=/poetry              \
    POETRY_REPOSITORIES_PALAIMON_URL=https://pypi.palaimon.io/

RUN apt-get update && apt-get install -y --no-install-recommends \
    wget curl                                                    \
    git                                                          \
    python3-dev                                                  \
    python3-pip

# uses $POETRY_VERSION & $POETRY_HOME internally
RUN curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python3 -
ENV PATH=${POETRY_HOME}/bin:${PATH}

COPY . /app

WORKDIR /app

RUN poetry install --no-dev

# poetry dependency resolution is slow
#RUN poetry add voila tqdm
RUN poetry run pip install voila tqdm

EXPOSE 8080

ENTRYPOINT ["poetry", "run", "voila", "--enable_nbextensions=True", "--no-browser", "--port=8080"]

CMD ["nbs/09_viola_example.ipynb"]