from fastapi import FastAPI, HTTPException, UploadFile, File, Depends
from fastapi.responses import StreamingResponse
from kitchenai.client import KitchenClient
from pydantic import BaseModel
import asyncio

app = FastAPI()

class QueryRequest(BaseModel):
    query: str

class MultiModalQueryRequest(BaseModel):
    query: str
    image_url: str

def get_kitchen_client():
    with KitchenClient(app_id="kitchenai", namespace="default") as client:
        yield client

@app.post("/keyword")
async def query(request: QueryRequest, client: KitchenClient = Depends(get_kitchen_client)):
    try:
        resp = client.query(request.query, "keyword-index-query")
        return {"response": resp}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/vector-index-query")
async def custom_node_query(request: QueryRequest, client: KitchenClient = Depends(get_kitchen_client)):
    try:
        resp = client.query(request.query, "vector-index-query")
        return {"response": resp}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/chromadb-embed")
async def file_upload(file: UploadFile = File(...), client: KitchenClient = Depends(get_kitchen_client)):
    try:
        contents = await file.read()
        resp = client.upload_file(contents, file.filename, "chromadb-embed")
        return {"message": resp}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

