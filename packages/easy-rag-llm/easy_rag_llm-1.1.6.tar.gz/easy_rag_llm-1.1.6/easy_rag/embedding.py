import numpy as np
from openai import OpenAI
from openai import AuthenticationError, APIConnectionError, RateLimitError, OpenAIError
from functools import lru_cache

class Embedding:
    def __init__(self, api_key, model="text-embedding-3-small"):
        self.api_key=api_key
        self.model=model
    
    @lru_cache(maxsize=10000)
    def create_embedding(self, text):
        try:
            client = OpenAI(api_key=self.api_key)
            response = client.embeddings.create(model=self.model, input=text)
            embedding = response.data[0].embedding
            return np.array(embedding, dtype=np.float32)

        except (AuthenticationError, APIConnectionError, RateLimitError, OpenAIError) as e:
            print(f"create_embedding has error: {e}")
            raise ValueError(f"OpenAI Error: {e}")
    
    def create_embeddings_batch(self, texts):
        """
        여러 텍스트를 한 번에 Embedding 요청.
        texts: 문자열 리스트
        return: 각 문자열에 대한 임베딩 리스트 (np.float32 형태)
        """
        try:
            client = OpenAI(api_key=self.api_key)
            response = client.embeddings.create(
                model=self.model,
                input=texts  # 리스트 형태로 전달
            )
            # response.data[i].embedding
            # 각 i번째 텍스트에 대한 임베딩이 담겨 있음.
            results = []
            for item in response.data:
                emb = np.array(item.embedding, dtype=np.float32)
                results.append(emb)
            return results

        except (AuthenticationError, APIConnectionError, RateLimitError, OpenAIError) as e:
            print(f"create_embeddings_batch error: {e}")
            raise ValueError(f"OpenAI Error: {e}")


