FROM python:3.8

RUN apt-get update
RUN apt-get install -y \
    libffi-dev \
    libssl-dev \
    libxml2-dev \
    libxslt-dev \
    libjpeg-dev \
    libfreetype6-dev \
    zlib1g-dev \
    net-tools

RUN mkdir -p factory
COPY . /factory

WORKDIR /factory

COPY requirements.txt .
RUN pip install -r requirements.txt

RUN dir -s


EXPOSE 8000
STOPSIGNAL SIGINT
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]