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
SECRET_KEY=some_key
DEBUG=True
POSTGRES_DB=some_db
POSTGRES_USER=postgres
POSTGRES_PASSWORD=some_password
DB_HOST=postgres_db
DB_PORT=some_port1
DB_OUT_PORT=some_port2
PRODUCTION_HOST=some_prod_host
```

Create and start the docker containers:

```sh
docker compose up -d
```

Open up the browser and navigate to the main page of the project at http://localhost:8001/.