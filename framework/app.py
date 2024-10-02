from flask import Flask, request
import json
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader, StorageContext, load_index_from_storage
import os
import logging

app = Flask(__name__)
PERSIST_DIR = "./framework/storage"
app.logger.setLevel(logging.INFO)


@app.route('/store', methods=['POST'])
def store():
    # check if storage already exists
    if not os.path.exists(PERSIST_DIR):
        # load the documents and create the index
        documents = SimpleDirectoryReader("framework/data").load_data()
        index = VectorStoreIndex.from_documents(documents)
        # store it for later
        index.storage_context.persist(persist_dir=PERSIST_DIR)
    else:
        # load the existing index
        storage_context = StorageContext.from_defaults(persist_dir=PERSIST_DIR)
        index = load_index_from_storage(storage_context)
        
    return json.dumps({'success': True}), 200, {
        'ContentType': 'application/json'}

@app.route('/query', methods=["POST"])
def query():
    app.logger.info(request.json)
    data = request.json
    storage_context = StorageContext.from_defaults(persist_dir=PERSIST_DIR)
    index = load_index_from_storage(storage_context)
    query_engine = index.as_query_engine()
    app.logger.info(data["query"])
    response = query_engine.query(data["query"])
    app.logger.info(response)

    return json.dumps({'msg': response.response}), 200, {
    'ContentType': 'application/json'}


app.run(port=8001)
