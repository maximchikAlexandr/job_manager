# JobManager
## About project

Project **JobManager** is a web application designed for the automation of management accounting. 


This project written in Python using the *Django* framework. For installation using the *Docker*,
the project contains two containers: the Django application 
and the *PostgreSQL* database.


## Installation

Clone the repository from GitHub:

```sh
git clone https://github.com/maximchikAlexandr/job_manager.git
```

Create a file named '.env' in the root directory:

```sh
cd job_manager/job_manager_proj/
nano .env
```

and fill it with the following environment variables:

```sh
# Django parameters
DEBUG=True
SECRET_KEY="the_key_used_for_encryption"
PRODUCTION_HOST=some_prod_host
DJANGO_SUPERUSER_PASSWORD="your_password"
DJANGO_SUPERUSER_EMAIL="your_email"
DJANGO_SUPERUSER_USERNAME="your_username"

# database parameters
POSTGRES_DB="database_name" 
POSTGRES_USER="your_database_username"
POSTGRES_PASSWORD="your_database_password"
DB_HOST="your_database_host"
DB_PORT="port_of_your_database_in_container"
DB_OUT_PORT="outer_port_of_your_database"

# Celery parameters
CELERY_HOST=redis
CELERY_PORT=6379

# Yandex disk
YANDEX_TOKEN="yandex_token_for_your_application"
YANDEX_SK="yandex_secret_key_for_opening_documents"

# Bitrix24
BX24_HOSTNAME="your_Bitrix24_host"
BX24_TOKEN_ADD="token_for_query_crm.deal.add"
BX24_TOKEN_UPDATE="token_for_query_crm.deal.update"
BX24_TOKEN_LIST="token_for_query_crm.deal.list"
```

Create and start the docker containers:

```sh
docker compose up -d
```

Open up the browser and navigate to the main page of the project at http://localhost:8001/.


## Yandex Disk


To use the application, you need to grant full access permissions to Yandex.Disk:

https://oauth.yandex.ru/client/new/id

To obtain an OAuth token:

https://yandex.ru/dev/id/doc/ru/access

## Bitrix24

Create three external webhooks in your Bitrix24 account:
https://helpdesk.bitrix24.com/open/12357038/


The webhooks are needed for the following methods:

1. crm.deal.add
2. crm.deal.update
3. crm.deal.list

API documentation of Bitrix24:

https://dev.1c-bitrix.ru/rest_help/

## API Documentation

Swagger is utilized for API documentation. If the application is deployed on the local machine, the documentation can be accessed through the following link:

http://localhost:8001/doc/