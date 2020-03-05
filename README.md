# Tesorio test

## DB Connection
The Postgres database can be accessed trough `localhost:8080`. The access credentials the DB are:

```
server= 'db'
username= 'postgres'
password= 'postgres'
dbname= 'tesorio'
```

## Deployment
The project can be deployed using `docker-compose` by running next command:
```
sudo docker-compose down && sudo docker-compose build --pull && sudo docker-compose up
```

The project comprises two endpoints:
* localhost:5000/save_data: Endpoint expecting a TXT file. Next you can find an example of a valid request to the endpoint
![Postman request](/temp/postman_request.png)
* localhost:5000/clean_db: Endpoint to clear the data uploaded so far
