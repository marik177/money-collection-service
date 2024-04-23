# Project Name
Service to provide a REST API for a simple CRUD application.

## Description
This service provides a money collection API. It allows users to create money collections on different occasions and make payments.


## Installation
### Start project using docker-compose

1. The first thing to do is to clone the repository:
    ```bash
    git clone https://github.com/marik177/money-collection-service.git
   ```
2. Using the Dockerfile and docker-compose.yaml build the project:
   ```bash
   docker compose build
    ```
3. Run Docker Compose to start the application:
    ```bash 
   docker compose up
    ```
4. Cretae the database schema:
    ```bash 
   docker compose exec django python manage.py migrate --settings=config.django.base

    ```
5. Create a superuser:
    ```bash
    docker compose exec django python manage.py createsuperuser --settings=config.django.base
     ```
6. Fill database with command:
    ```bash
    docker compose exec django python manage.py fill_mock_data --settings=config.django.base
    ```
7. The application will be available at http://localhost:8000
8. The admin panel will be available at http://localhost:8000/admin
9. Documentation will be available at http://localhost:8000/docs
10. To stop the Docker container, use the following command:
    ```bash 
   docker-compose down -v
    ```

## Usage
#### On creatin collection author will be notified by email
#### On payment creation contributor will be notified by email

