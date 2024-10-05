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

@app.post("/query")
async def query(request: QueryRequest, client: KitchenClient = Depends(get_kitchen_client)):
    try:
        resp = client.query(request.query, "query-1")
        return {"response": resp}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/streaming-query")
async def streaming_query(request: QueryRequest, client: KitchenClient = Depends(get_kitchen_client)):
    try:
        resp = client.query(request.query, "streaming")
        return StreamingResponse(resp, media_type="text/event-stream")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/hybrid-search")
async def hybrid_search(request: QueryRequest, client: KitchenClient = Depends(get_kitchen_client)):
    try:
        resp = client.query(request.query, "hybrid-search")
        return {"results": resp}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/multi-modal-query")
async def multi_modal_query(request: MultiModalQueryRequest, client: KitchenClient = Depends(get_kitchen_client)):
    try:
        resp = client.query({"query": request.query, "image_url": request.image_url}, "multi-modal-query")
        return {"response": resp}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/custom-node-query")
async def custom_node_query(request: QueryRequest, client: KitchenClient = Depends(get_kitchen_client)):
    try:
        resp = client.query(request.query, "custom-node-parsing")
        return {"response": resp}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/upload")
async def upload_file(file: UploadFile = File(...), client: KitchenClient = Depends(get_kitchen_client)):
    try:
        contents = await file.read()
        resp = client.upload_file(contents, file.filename, "embed-1")
        return {"message": resp}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/multi-modal-upload")
async def multi_modal_upload(file: UploadFile = File(...), client: KitchenClient = Depends(get_kitchen_client)):
    try:
        contents = await file.read()
        resp = client.upload_file(contents, file.filename, "multi-modal-embed")
        return {"message": resp}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/custom-parse-upload")
async def custom_parse_upload(file: UploadFile = File(...), client: KitchenClient = Depends(get_kitchen_client)):
    try:
        contents = await file.read()
        resp = client.upload_file(contents, file.filename, "custom-parse-embed")
        return {"message": resp}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
