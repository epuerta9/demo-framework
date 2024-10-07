import json
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader, StorageContext, load_index_from_storage
from llama_index.core import SimpleKeywordTableIndex, Document
from llama_index.core.node_parser import SentenceSplitter

from llama_index.core.node_parser import SimpleNodeParser
from llama_index.core.query_engine import RetrieverQueryEngine
from llama_index.core.postprocessor import SimilarityPostprocessor
from llama_index.core import SimpleDirectoryReader
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
from llama_index.core import SimpleKeywordTableIndex
import chromadb
from llama_index.vector_stores.chroma import ChromaVectorStore
from llama_index.core import PromptTemplate

# initialize client, setting path to save data
db = chromadb.PersistentClient(path="./chroma_db")

# create collection
chroma_collection = db.get_or_create_collection("quickstart")

vector_store = ChromaVectorStore(chroma_collection=chroma_collection)


class QueryRequest(BaseModel):
    query: str

class MultiModalQueryRequest(BaseModel):
    query: str
    image_url: str
app = FastAPI()
kitchen = KitchenAIApp(app_instance=app)


Settings.llm = OpenAI(model="gpt-4")
Settings.chunk_size = 1024


#https://docs.llamaindex.ai/en/stable/examples/query_engine/ensemble_query_engine/


@kitchen.query("keyword-index-query")
async def keyword_index_query(request: Request, body: QueryRequest):
   # Retrieve all documents from Chroma
    results = chroma_collection.get(include=["documents", "metadatas", "embeddings"])
    
    # Convert Chroma results to LlamaIndex nodes
    parser = SentenceSplitter()

    documents = [Document(text=t) for t in results["documents"]]
    nodes = parser.get_nodes_from_documents(documents)

    storage_context = StorageContext.from_defaults(vector_store=vector_store)
    QA_PROMPT_TMPL = (
        "Context information is below.\n"
        "---------------------\n"
        "{context_str}\n"
        "---------------------\n"
        "Given the context information and not prior knowledge, "
        "answer the question. If the answer is not in the context, inform "
        "the user that you can't answer the question - DO NOT MAKE UP AN ANSWER.\n"
        "In addition to returning the answer, also return a relevance score as to "
        "how relevant the answer is to the question. "
        "Question: {query_str}\n"
        "Answer (including relevance score): "
    )

    keyword_index = SimpleKeywordTableIndex(
        nodes,
        storage_context=storage_context,
        show_progress=True,
    )

    QA_PROMPT = PromptTemplate(QA_PROMPT_TMPL)

    keyword_query_engine = keyword_index.as_query_engine(
        text_qa_template=QA_PROMPT
    )
    
    
    response = keyword_query_engine.query(body.query)

    print(response)
    
    return {"response": str(response)}


@kitchen.query("vector-index-query")
async def vector_index_query(request: Request, body: QueryRequest):
    # Custom node parser
    node_parser = SimpleNodeParser.from_defaults(
        chunk_size=50,
        chunk_overlap=10,
        paragraph_separator="\n\n",
        include_metadata=True,
        include_prev_next_rel=True
    )
    
    storage_context = StorageContext.from_defaults(vector_store=vector_store)

    vector_index = VectorStoreIndex.from_vector_store(vector_store, storage_context=storage_context)

    
    query_engine = vector_index.as_query_engine(
        node_parser=node_parser,
        retriever_mode="all_leaf",
        response_mode="tree_summarize",
    )
    
    response = query_engine.query(body.query)
    
    return {"response": str(response)}

@kitchen.storage("chromadb-embed")
async def custom_parse_embed(request: Request, file: UploadFile = File(...)):
    try:
        contents = await file.read()
        filename = file.filename
        
        file_path = f"./uploads/{filename}"
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, "wb") as f:
            f.write(contents)
        
        # Load and parse documents
        documents = SimpleDirectoryReader(input_files=[file_path]).load_data()
        storage_context = StorageContext.from_defaults(vector_store=vector_store)


        VectorStoreIndex.from_documents(documents=documents, storage_context=storage_context)
        

        return {"message": f"File {filename} uploaded and processed with custom node parsing"}
    except Exception as e:
        logging.error(f"Error processing custom parsed upload: {str(e)}")
        return {"error": str(e)}
