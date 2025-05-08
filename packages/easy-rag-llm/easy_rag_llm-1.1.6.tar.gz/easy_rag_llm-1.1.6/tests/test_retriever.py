import os
import sys
import numpy as np

from dotenv import load_dotenv

load_dotenv()
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../")))

from easy_rag.embedding import Embedding
from easy_rag.retriever import Retriever
from easy_rag.index import IndexManager
from easy_rag.agent import Agent
from easy_rag.rag_service import RagService

def test_rag_service():
    rag_service = RagService(
        embedding_model="text-embedding-3-small",
        response_model="openai",
        open_api_key=os.getenv("OPENAI_API_KEY"),
    )

    resource_path = "./tests/resources"

    # 리소스 로드 및 인덱스 생성
    index, metadata = rag_service.rsc(resource_path, force_update=True)

    assert index.ntotal > 0, "Index should contain data."
    assert len(metadata) > 0, "Metadata should not be empty."

