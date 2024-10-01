import logging
import requests
import os
import argparse
import json

logging.basicConfig(level=logging.INFO)

# Step 1: Create an ArgumentParser object
parser = argparse.ArgumentParser(description="A script that processes positional arguments.")

# Step 2: Add positional arguments
# The first positional argument 'input_file'
parser.add_argument('action', type=str, help="The input file to be processed")

# Optional argument (example)
parser.add_argument('--query', type=str, help="A query string to be processed")

# Step 3: Parse the arguments
args = parser.parse_args()


base_url = os.getenv('BASE_URL', 'http://localhost') + ':' + os.getenv(
                    'DAPR_HTTP_PORT', '3500')

# Adding app id as part of the header
headers = {'dapr-app-id': 'kitchenai', 'content-type': 'application/json'}

if args.query and args.action == "query":
    data = {
        'query': args.query,
    }
    print(data)
    # Invoking a service
    result = requests.post(
        url='%s/query' % (base_url),
        data=json.dumps(data),
        headers=headers
    )

    print(f"Response: {result.text}")

if args.action == "store":
    # Invoking a service
    result = requests.post(
        url='%s/store' % (base_url),
        headers=headers
    )

    print(f"Response: {result.text}")