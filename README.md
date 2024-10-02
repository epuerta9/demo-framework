# demo-framework

Simple demo to showcase AI framework abstraction using dapr 

## Pre-reqs

1. install dapr cli 

https://docs.dapr.io/getting-started/install-dapr-cli/


## QuickStart

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
