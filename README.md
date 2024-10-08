# demo-framework

Simple demo to showcase AI framework abstraction using dapr 



# Quickstart 

1. build the kitchenai side car 
  `make build-s6`

2. export OPENAI_API_KEY env variable with your open api key 
  `export OPENAI_API_KEY=yourkey`

2. enter the sidecar 
  `make dev`
  run the dev script by running the dev command 
    `dev` 
  This will start up both the dapr client for the kitchenAI and will also start up the app dapr client 

2. run the authored cookbook with fastapi
  `fastapi dev framework/app.py --host 0.0.0.0`
  This will spin up the fastapi on port :8000 which you can interact with directly 

3. spin up the client application manually 

  `cd client`
  `python -m venv venv`
  `source venv/bin/activate`
  `pip install -r requirements.txt`
  `fastapi dev app.py --port 8001` so ports don't conflict 

4. Still Work in progress but you should now be able to open localhost:8001 on the application side and communicate with 
  the kitchenai container through the dapr sidecars. 

  the authored library contains a way to section off certain cookbook sections. It sits on top of fastapi and dapr

  ### Known Issues 
    Still troubleshooting why sometimes the dapr sidecars don't communicate with each other. They are sensitive to mDNS which is how they do service discovery. Ironing out this section is an important part of making kitchenAI cookbooks portable and microservice ready. 

    Currently using direct service invocation dapr capability to communicate from app -> app sidecar -> kitchen sidecar -> cookbook










## Pre-reqs

1. install dapr cli 

https://docs.dapr.io/getting-started/install-dapr-cli/



## Developing

        tested with: python version 3.11+

1. `make deps`
2. run framework api `make run-framework`
3. go to the client directory and activate environment `cd client && source venv/bin/activate` 
4. run client commands 
    1. store example data in vector `dapr run  --app-id client --app-protocol http --dapr-http-port 3500 -- python3 app.py store`
    2. run queries against it `dapr run  --app-id client --app-protocol http --dapr-http-port 3500 -- python3 app.py query --query 'can you summarize this text?'`


# Build Folder 
To pass build arguments declaratively, you can use a Docker Compose file or a Kubernetes manifest, depending on your deployment environment. Here's how you can do it for both cases:

Using Docker Compose:

Create or update your docker-compose.yml file:

```
yamlCopyversion: '3.8'

services:
  your-service-name:
    build:
      context: .
      dockerfile: Dockerfile
      args:
        APP_DIR: ./your_custom_dir
        REQUIREMENTS_FILE: your_custom_requirements.txt
```