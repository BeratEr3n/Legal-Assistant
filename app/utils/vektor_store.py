import os
from typing import List
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct
import google.generativeai as genai
from langchain.schema import Document
from qdrant_client.http.exceptions import UnexpectedResponse
from dotenv import load_dotenv

load_dotenv()

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=GOOGLE_API_KEY)

class GeminiEmbeddings:
    """
        Google Gemini API'sini kullanarak metin gömme (embedding) işlemleri yapar.
    """

    def __init__(self, model_name="models/embedding-001"):
        self.model_name = model_name

    # Birden çok metin için embedding oluşturur.
    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        return [self.embed_query(text) for text in texts]

    # Tek bir metin için embedding oluşturur.
    def embed_query(self, text: str) -> List[float]:
        result = genai.embed_content(
            model=self.model_name,
            content=text,
            task_type="retrieval_document"
        )
        return result['embedding']

# Qdrant vektör deposunu başlatır.
def initialize_vector_store(collection_name: str):
    client = QdrantClient(
        url=os.getenv("QDRANT_URL"),
        api_key=os.getenv("QDRANT_API_KEY", None)
    )

    embeddings = GeminiEmbeddings()

    try:
        client.get_collection(collection_name)
    except UnexpectedResponse as e:
        if e.status_code == 404:
            client.create_collection(
                collection_name=collection_name,
                vectors_config=VectorParams(
                    size=768,  # Gemini embedding boyutu
                    distance=Distance.COSINE
                )
            )

    return client, embeddings

# Belgeleri vektör deposuna ekler.
def add_to_vector_store(client, embeddings, documents, collection_name: str):

    points = []
    for i, doc in enumerate(documents):
        embedding = embeddings.embed_query(doc.page_content)
        points.append(
            PointStruct(
                id=i,
                vector=embedding,
                payload={
                    "text": doc.page_content,
                    "metadata": doc.metadata
                }
            )
        )

    client.upsert(
        collection_name=collection_name,
        points=points
    )

# Vektör deposunda sorgu yapar ve LangChain Document formatına dönüştürür.
def query_vector_store(client, embeddings, query: str, collection_name: str, k: int = 6):
    
    query_embedding = embeddings.embed_query(query)

    results = client.search(
        collection_name=collection_name,
        query_vector=query_embedding,
        limit=k
    )

    documents = []
    for result in results:
        documents.append(
            Document(
                page_content=result.payload['text'],
                metadata=result.payload['metadata']
            )
        )

    return documents