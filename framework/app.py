import json
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader, StorageContext, load_index_from_storage
from llama_index.core.node_parser import SimpleNodeParser
from llama_index.core.query_engine import RetrieverQueryEngine
from llama_index.core.postprocessor import SimilarityPostprocessor
from llama_index.multi_modal_llms import OpenAIMultiModal
from llama_index.multi_modal_llms.openai import OpenAIMultiModal
from llama_index.core import MultiModalVectorStoreIndex, SimpleDirectoryReader
import os
import logging
from kitchenai_sdk.kitchenai import KitchenAIApp
from fastapi import Request, FastAPI, File, UploadFile
from llama_index.llms.openai import OpenAI
from pydantic import BaseModel
from fastapi.responses import StreamingResponse
import asyncio
from llama_index.llms.openai import OpenAI
from llama_index.core import Settings
class QueryRequest(BaseModel):
    query: str

class MultiModalQueryRequest(BaseModel):
    query: str
    image_url: str
app = FastAPI()
kitchen = KitchenAIApp(app_instance=app)


Settings.llm = OpenAI(model="gpt4")
Settings.chunk_size = 1024


#https://docs.llamaindex.ai/en/stable/examples/query_engine/ensemble_query_engine/

@kitchen.query("hybrid-search")
async def hybrid_search(request: Request, body: QueryRequest):
    storage_context = StorageContext.from_defaults(persist_dir="storage")
    index = load_index_from_storage(storage_context)
    
    # Create a BM25Retriever
    bm25_retriever = BM25Retriever.from_defaults(index=index, similarity_top_k=2)
    
    # Create a vector retriever
    vector_retriever = index.as_retriever(similarity_top_k=2)
    
    # Combine retrievers
    retriever = RetrieverQueryEngine.from_args(
        vector_retriever, node_postprocessors=[SimilarityPostprocessor(similarity_cutoff=0.7)]
    )
    
    # Hybrid search
    response = retriever.retrieve(body.query)
    
    return {"results": [node.node.text for node in response]}

@kitchen.query("multi-modal-query")
async def multi_modal_query(request: Request, body: MultiModalQueryRequest):
    storage_context = StorageContext.from_defaults(persist_dir="multi_modal_storage")
    index = load_index_from_storage(storage_context)
    
    query_engine = index.as_query_engine(multi_modal_llm=multi_modal_llm)
    
    response = query_engine.query({
        "text": body.query,
        "image": body.image_url
    })
    
    return {"response": str(response)}


@kitchen.query("custom-node-parsing")
async def custom_node_parsing(request: Request, body: QueryRequest):
    # Custom node parser
    node_parser = SimpleNodeParser.from_defaults(
        chunk_size=50,
        chunk_overlap=10,
        paragraph_separator="\n\n",
        include_metadata=True,
        include_prev_next_rel=True
    )
    
    storage_context = StorageContext.from_defaults(persist_dir="custom_parsed_storage")
    index = load_index_from_storage(storage_context)
    
    query_engine = index.as_query_engine(
        node_parser=node_parser,
        retriever_mode="all_leaf",
        response_mode="tree_summarize",
    )
    
    response = query_engine.query(body.query)
    
    return {"response": str(response)}

@kitchen.storage("custom-parse-embed")
async def custom_parse_embed(request: Request, file: UploadFile = File(...)):
    try:
        contents = await file.read()
        filename = file.filename
        
        file_path = f"./uploads/{filename}"
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, "wb") as f:
            f.write(contents)
        
        # Custom node parser
        node_parser = SimpleNodeParser.from_defaults(
            chunk_size=50,
            chunk_overlap=10,
            paragraph_separator="\n\n",
            include_metadata=True,
            include_prev_next_rel=True
        )
        
        # Load and parse documents
        documents = SimpleDirectoryReader(input_files=[file_path]).load_data()
        nodes = node_parser.get_nodes_from_documents(documents)
        
        # Create index with custom parsed nodes
        index = VectorStoreIndex(nodes)
        
        # Persist the index
        index.storage_context.persist(persist_dir="custom_parsed_storage")

        return {"message": f"File {filename} uploaded and processed with custom node parsing"}
    except Exception as e:
        logging.error(f"Error processing custom parsed upload: {str(e)}")
        return {"error": str(e)}
