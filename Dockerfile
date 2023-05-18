ARG PYTHON_VERSION=3.11-slim-bullseye

# pull official base image
FROM python:${PYTHON_VERSION}

# set work directory
WORKDIR /app

# install dependencies
RUN pip install --upgrade pip
COPY requirements-base.txt requirements-base.txt
RUN pip install -r requirements-base.txt

# copy project
COPY . .

CMD [ \
    "gunicorn", \
    "--workers", \
    "4", \
    "--worker-class", \
    "gevent", \
    "-b", \
    "0.0.0.0", \
    "flow2and4.app:create_app(mode='prod')" \
    ]

