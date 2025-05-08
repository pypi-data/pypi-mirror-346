import os
import faiss
import json

"""
class IndexManager:
    def save(self, index, metadata, index_file="faiss_index.bin", metadata_file="metadata.json"):
        faiss.write_index(index, index_file)
        with open(metadata_file, "w") as f:
            json.dump(metadata, f)
        print(f"Index saved to {index_file}, metadata saved to {metadata_file}")

    def load(self, index_file="faiss_index.bin", metadata_file="metadata.json"):
        if not os.path.exists(index_file) or not os.path.exists(metadata_file):
            print("Index or metadata file not found.")
            return None, None
        index = faiss.read_index(index_file)
        with open(metadata_file, "r") as f:
            metadata = json.load(f)
        print(f"Index loaded from {index_file}, metadata loaded from {metadata_file}")
        return index, metadata
"""

class IndexManager:
    def save(self, index, metadata, resource_path, index_file="faiss_index.bin", metadata_file="metadata.json"):
        rsc_folder_name = os.path.basename(resource_path)
        rsc_index_dir = f"{rsc_folder_name}Index"

        if not os.path.exists(rsc_index_dir):
            os.makedirs(rsc_index_dir)

        index_file_path = os.path.join(rsc_index_dir, index_file)
        metadata_file_path = os.path.join(rsc_index_dir, metadata_file)

        faiss.write_index(index, index_file_path)
        with open(metadata_file_path, "w") as f:
            json.dump(metadata, f)

        print(f"Index saved to {index_file_path}, metadata saved to {metadata_file_path}")

    def load(self, resource_path, index_file="faiss_index.bin", metadata_file="metadata.json"):
        rsc_folder_name = os.path.basename(resource_path)
        rsc_index_dir = f"{rsc_folder_name}Index"

        index_file_path = os.path.join(rsc_index_dir, index_file)
        metadata_file_path = os.path.join(rsc_index_dir, metadata_file)

        if not os.path.exists(index_file_path) or not os.path.exists(metadata_file_path):
            print("Index or metadata file not found.")
            return None, None

        index = faiss.read_index(index_file_path)
        with open(metadata_file_path, "r") as f:
            metadata = json.load(f)

        print(f"Index loaded from {index_file_path}, metadata loaded from {metadata_file_path}")
        return index, metadata