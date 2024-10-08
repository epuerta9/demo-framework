

deps: deps-framework deps-client

deps-framework:
	cd framework && \
	python3 -m venv venv && \
	. venv/bin/activate && \
	pip install -r requirements.txt

deps-client:
	cd client && \
	python3 -m venv venv && \
	. venv/bin/activate && \
	pip install -r requirements.txt


run: run-framework run-client-sidecar

run-framework:
	. framework/venv/bin/activate && \
	dapr run --app-port 8001  --app-id kitchenai --app-protocol http --config dapr/config.yml --log-level debug --dapr-http-port 3501 -- python3 framework/app.py

run-client-sidecar:
	dapr run  --app-id client --app-protocol http --log-level debug --config dapr/config.yml --dapr-http-port 3500

e2e:
	docker compose -f docker/docker-compose.s2s.yml up -d 	

cmd := up -d

dev:
	docker run -it --entrypoint /bin/bash -v $(shell pwd):/app/kitchenai -e OPENAI_API_KEY=$$OPENAI_API_KEY \
	-p 8000:8000 \
	-p 3500:3500 \
	s6

s6:
	docker compose -f docker/docker-compose.s6.yml $(cmd) 

all-in-one: build-s6 build-client
	docker compose -f docker/docker-compose.allinone.yml $(cmd)

compose-all-in-one:
	docker compose -f docker/docker-compose.allinone.yml $(cmd)

build-s6:
	docker build  -t s6 --no-cache -f docker/Dockerfile.s6 .

build-client:
	docker build  -t kitchen-client --no-cache -f docker/Dockerfile.client .

clean:
	docker compose -f docker/docker-compose.s2s.yml down