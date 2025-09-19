FROM python:3.10.2-slim-bullseye

ENV PIP_DISABLE_PIP_VERSION_CHECK 1
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt-get update -y && \
    apt-get install -y libpq-dev gcc && \
    apt-get install -y logrotate && \
    apt-get install -y libcairo2 libcairo2-dev libpangocairo-1.0-0 && \
    apt-get install -y gettext && \
    pip install --upgrade pip

COPY ./requirements.txt .
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

COPY . /code

# Build user documentation
WORKDIR /code/documentation/user
RUN mkdocs build

# Build admin documentation
WORKDIR /code/documentation/admin
RUN mkdocs build

WORKDIR /code

RUN chmod +x /code/entrypoint.sh
ENTRYPOINT ["sh", "/code/entrypoint.sh"]