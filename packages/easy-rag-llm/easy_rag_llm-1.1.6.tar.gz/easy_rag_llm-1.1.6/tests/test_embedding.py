import os
import sys

from dotenv import load_dotenv

load_dotenv() 
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../")))
from easy_rag.embedding import Embedding

def test_embedding():

    api_key = os.getenv("OPENAI_API_KEY")
    embedding = Embedding(api_key=api_key)
    
    text = "This is a test sentence."
    vector = embedding.create_embedding(text)
    
    assert vector.shape == (1536,), "Unexpected embedding size."
