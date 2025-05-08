import os
import sys

from dotenv import load_dotenv

load_dotenv()
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../")))

from easy_rag import RagService

def test_rag_service():
    rag_service = RagService(
        embedding_model="text-embedding-3-small",
        response_model="openai",
        open_api_key=os.getenv("OPENAI_API_KEY"),
    )

    resource_path = "./tests/resources"
    os.makedirs(resource_path, exist_ok=True)
    with open(f"{resource_path}/test.pdf", "w") as f:
        f.write("Sample PDF content for testing.")

    index, metadata = rag_service.rsc(resource_path, force_update=True)

    assert index.ntotal > 0, "Index should contain data."
    assert len(metadata) > 0, "Metadata should not be empty."

    query = "What is the content of test.pdf?"
    response = rag_service.generate_response((index, metadata), query)

    assert isinstance(response, str), "Response should be a string."
