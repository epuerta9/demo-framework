# Client

starting up the client with it's appropriate dapr side car 

1. app-id: client

## Store

`dapr run  --app-id client --app-protocol http --dapr-http-port 3500 -- python3 app.py store`

## Query

`dapr run  --app-id client --app-protocol http --dapr-http-port 3500 -- python3 app.py query 'query'`


## Raw HTTP query 

you can query the flask application without the dapr proxy 

`curl -X POST -d '{"query":"what is the authors name"}' -H "Content-Type: application/json" http://localhost:8001/query`