#!/bin/bash

dapr run  \
    --app-id app \
    --app-protocol http \
    --scheduler-host-address "" \
    --dapr-http-port 3500 &

dapr run --app-port 8000 \
    --app-id kitchenai \
    --app-protocol http \
    --scheduler-host-address "" \
    --dapr-http-port 3501 & 


fastapi dev /app/kitchenai/app.py 