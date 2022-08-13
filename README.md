# Flask & PostgreSQL

Project is aimed to create a contenerized environment using Flask backand with connection to the PostgreSQL database with a connection using REST API.

## Files and foldrs description 

* `app.py` - main flask application file that hosts a server for rest api communication between the client and postgres database

* `config.py` - confguration file that holds a Config class which reads mandatory environmental variables

* `docker-compose.yml` - docker container description file, which is responsible for starting both flask and postgres containers 

* `Dockerfile` - docker file that describes a custom flask image 

* `requirements.txt` - python package dependencies

## Docker setup

`docker-compose up --build`

## REST API examples 

To check if the table exists: 

```
    curl -X POST -H "Content-type: application/json" -d "{\"table_name\" : \"employee\"}" "localhost:5000/check"
```

To apply sql commands on the postgresql database:

```
    curl -X POST -H "Content-type: application/json" -d "{\"sql_command\" : < sql_command >}" localhost:5000/create
```