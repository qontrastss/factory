# Factory project

This repository contains a Django project with Celery and Redis integrated, all managed and deployed with Docker Compose. Follow these steps to quickly set up and run the project.

## Prerequisites

Ensure you have the following software installed on your system:

- [Docker](https://docs.docker.com/get-docker/)
- [Docker Compose](https://docs.docker.com/compose/install/)

## Getting Started

1. Clone the repository to your local machine:

   ```bash
   git clone <repository_url>
   cd factory

2. Create a .env file and configure your environment variables. You can use the provided .env.example as a template.
   ```bash
    cp .env.example .env

4. Run Django app
     ```bash
     python manage.py runserver
5. Run Celery worker
     ```bash
      celery -A factory worker -l INFO

6. Or by build and start the Docker containers using Docker Compose:
     ```bash
    docker-compose up -d

## Features

- **Swagger Schema Generator** - Schema uses drf-yasg library for generating Swagger Schema.And can be accessed by /swagger route

- **Token Auth** - Configured Django Rest Framework for Token Authentication System.
  
- **Tests** - The tests were covered using the pytest library.

## Quickstart
You can find list of API [here](https://galiash.site/swagger/)
In order to work after registration you should connect with telegram bot by sending username and password to him.
