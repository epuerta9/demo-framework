

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


run-framework:
	cd framework && \
	. venv/bin/activate && \
	dapr run --app-port 8001  --app-id framework-1 --app-protocol http --dapr-http-port 3501 -- python3 app.py

