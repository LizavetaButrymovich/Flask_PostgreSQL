# Flask & PostgreSQL

Project is aimed to create a contenerized environment using Flask backand with connection to the PostgreSQL database with a connection using REST API.

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