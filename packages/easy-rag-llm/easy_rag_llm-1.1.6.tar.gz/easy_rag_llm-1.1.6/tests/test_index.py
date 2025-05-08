import os
import sys
import numpy as np
import faiss

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../")))
from easy_rag.index import IndexManager

def test_index_manager():
    index_manager = IndexManager()

    d = 128
    index = faiss.IndexFlatL2(d)
    data = np.random.random((10, d)).astype(np.float32)
    index.add(data)
    metadata = [{"id": i, "info": f"Document {i}"} for i in range(10)]

    index_file = "./tests/faiss_index.bin"
    metadata_file = "./tests/metadata.json"
    os.makedirs("./tests", exist_ok=True)

    index_manager.save(index, metadata, index_file, metadata_file)

    loaded_index, loaded_metadata = index_manager.load(index_file, metadata_file)

    assert loaded_index.ntotal == index.ntotal, "Loaded index does not match."
    assert loaded_metadata == metadata, "Loaded metadata does not match."
