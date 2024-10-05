import json
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader, StorageContext, load_index_from_storage
import os
import logging
from kitchenai_sdk.kitchenai import KitchenAIApp
from fastapi import Request, FastAPI
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader
from llama_index.llms.openai import OpenAI
from llama_index.core import StorageContext, load_index_from_storage
from pydantic import BaseModel
from fastapi.responses import StreamingResponse
import asyncio

class QueryRequest(BaseModel):
    query: str

app = FastAPI()
kitchen = KitchenAIApp(app_instance=app)
llm = OpenAI(model="gpt-4")

async def astreamer(generator):
    try:
        for i in generator:
            yield (i)
            await asyncio.sleep(.1)
    except asyncio.CancelledError as e:
        
        print('cancelled')

@kitchen.query("query-1")
def query2(request: Request, body: QueryRequest):

    print(body)
    # rebuild storage context
    storage_context = StorageContext.from_defaults(persist_dir="storage")

    # load index
    index = load_index_from_storage(storage_context)

    chat_engine = index.as_chat_engine(chat_mode="best", llm=llm, verbose=True)

    response = chat_engine.chat(
        body.query
    )
    return {"msg": response}

@kitchen.query("streaming")
def query2(request: Request, body: QueryRequest):

    # rebuild storage context
    storage_context = StorageContext.from_defaults(persist_dir="storage")

    # load index
    index = load_index_from_storage(storage_context)

    query_engine = index.as_query_engine(streaming=True, similarity_top_k=1)

    stream = query_engine.query(body.query)
    return StreamingResponse(astreamer(stream.response_gen), media_type="text/event-stream")

@kitchen.query("query-2")
def query2(request: Request, body: QueryRequest):

    print(body)
    # rebuild storage context
    storage_context = StorageContext.from_defaults(persist_dir="storage")

    # load index
    index = load_index_from_storage(storage_context)

    chat_engine = index.as_chat_engine(chat_mode="best", llm=llm, verbose=True)

    response = chat_engine.chat(
        "What are the first programs Paul Graham tried writing?"
    )
    return {"msg": "success-modified"}


@kitchen.storage("embed-1")
async def embed_1(request: Request):
    try:
        # Get the content type from headers
        content_type = request.headers.get("content-type", "")
        
        if "multipart/form-data" in content_type:
            # Handle multipart form data (traditional file upload)
            form = await request.form()
            uploaded_file = form["file"]
            contents = await uploaded_file.read()
            filename = uploaded_file.filename
        else:
            # Handle raw file content (as sent by KitchenClient)
            contents = await request.body()
            filename = request.headers.get("filename", "uploaded_file")
        
        # Save the file
        file_path = f"./uploads/{filename}"
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, "wb") as f:
            f.write(contents)
        
        # Process the file (example: add to index)
        new_docs = SimpleDirectoryReader(input_files=[file_path]).load_data()
        index = VectorStoreIndex.from_documents(new_docs)
        index.storage_context.persist(persist_dir="storage")

        return {"message": f"File {filename} uploaded and processed successfully"}
    except Exception as e:
        logging.error(f"Error processing upload: {str(e)}")
        return {"error": str(e)}



