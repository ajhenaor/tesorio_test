# Tesorio test

## DB Connection
The admin panel can be accessed trough `localhost:8080`. The credentials to access the DB are:

```
host= 'db'
dbname= 'tesorio'
user= 'postgres'
password= 'postgres'
```

## Deployment
The project can be deployed using `docker-compose` by running next command:
```
sudo docker-compose down && sudo docker-compose build --pull && sudo docker-compose up
```

The project comprises two endpoints:
* localhost:5000/save_data: Endpoint expecting a TXT file in order to insert it in the Postgres DB. Next is an example of a valid request to the endpoint
```
curl --location --request GET 'http://localhost:5000/save_data' \
--header 'Content-Type: application/json' \
--form 'myfile= [insert path to txt file]'
```
* localhost:5000/clean_db: Endpoint to clear the data uploaded so far
