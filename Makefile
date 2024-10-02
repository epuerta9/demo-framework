

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

clean:
	docker compose -f docker/docker-compose.s2s.yml down