import requests
import numpy as np
from openai import OpenAI
import json
import openai

class Agent:
    def __init__(self, embedding_model, model, open_api_key=None, deepseek_api_key=None, deepseek_base_url=None):
        self.model = model
        self.embedding_model = embedding_model
        self.open_api_key = open_api_key
        self.deepseek_api_key = deepseek_api_key
        self.deepseek_base_url = deepseek_base_url
        self.last_prompt = None
        self.context_expansion = False
        self.expansion_window = 1  # 앞뒤로 몇 개의 청크를 포함할지 설정

    def set_context_expansion(self, enable: bool, window_size: int = 1):
        """컨텍스트 확장 설정을 변경합니다.
        
        Args:
            enable (bool): 컨텍스트 확장 기능 활성화 여부
            window_size (int): 앞뒤로 포함할 청크의 수
        """
        self.context_expansion = enable
        self.expansion_window = max(1, window_size)  # 최소 1

    def expand_context(self, metadata, selected_indices):
        """선택된 인덱스의 앞뒤 컨텍스트를 포함하여 확장된 컨텍스트를 반환합니다.
        
        Args:
            metadata (list): 전체 메타데이터 리스트
            selected_indices (list): 선택된 인덱스 리스트
        
        Returns:
            list: 확장된 컨텍스트 리스트
        """
        if not self.context_expansion:
            return [metadata[idx] for idx in selected_indices if idx < len(metadata)]

        expanded_contexts = []
        seen_indices = set()

        for idx in selected_indices:
            if idx >= len(metadata):
                continue

            # 현재 문서의 파일명과 페이지 번호
            current_file = metadata[idx]['file_name']
            current_page = metadata[idx]['page_number']

            # 확장 범위 계산
            start_idx = max(0, idx - self.expansion_window)
            end_idx = min(len(metadata) - 1, idx + self.expansion_window)

            # 앞뒤 컨텍스트 수집
            for i in range(start_idx, end_idx + 1):
                if i in seen_indices:
                    continue
                    
                # 같은 파일의 연속된 페이지만 포함
                if (metadata[i]['file_name'] == current_file and 
                    abs(metadata[i]['page_number'] - current_page) <= self.expansion_window):
                    expanded_contexts.append(metadata[i])
                    seen_indices.add(i)

        return expanded_contexts

    def default_query_embedding_fn(self, query, index_dim): # 테스트용 가짜 임베딩
        return np.random.random(index_dim).astype(np.float32)
    
    def real_query_embedding_fn(self, query, index_dim_f): # 실제 임베딩, dim_f 안씀   
        client = OpenAI(api_key=self.open_api_key)
        response = client.embeddings.create(model=self.embedding_model, input=query)
        embedding = response.data[0].embedding
        return np.array(embedding, dtype=np.float32)

    def generate_response(self, resource, query, return_prompt=False, evidence_num=3):
        index, metadata = resource
        TOP_K = evidence_num
        query_embedding = self.real_query_embedding_fn(query, index.d)
        distances, indices = index.search(query_embedding.reshape(1, -1), TOP_K)
        

        if indices.size == 0 or len(indices[0]) == 0:
            raise ValueError("No relevant evidence found.")

        # 컨텍스트 확장 적용
        evidence = self.expand_context(metadata, indices[0])
        if not evidence:
            raise ValueError("No valid evidence found.")

        """ legacy code
        formatted_evidence = "\n".join(
            [f"File: {e['file_name']}, Page: {e['page_number']}, Text: {e['text']}" for e in evidence[:TOP_K]]
        )
        """
        # capsulate with JSON
        formatted_evidence = json.dumps(
            [{"file_name": e['file_name'], "page_number": e['page_number'], "text": e['text']} for e in evidence],
            indent=4, ensure_ascii=False
        )


        prompt = f"""
        System: The following is the most relevant information from the Knowledge for your query.
        Given format of the Knowledge is JSON with the following structure:
        {{
            "file_name": "string",
            "page_number": "integer",
            "text": "string"
        }}
        Always answer in the same language as the User prompt and strictly based on the provided Knowledge.
        Do not speculate or create information beyond what is given.
        ==== Knowledge: start ====
        {formatted_evidence}
        ==== Knowledge: end ====

        User: Below is the User prompt:
        ==== User prompt: start ====
        {query}
        ==== User prompt: end ====
        """
        self.last_prompt = prompt.strip()
        if return_prompt:
            print(prompt)
            return self.last_prompt

        if self.model == "deepseek-chat":
            headers = {
                "Authorization": f"Bearer {self.deepseek_api_key}",
                "Content-Type": "application/json",
            }
            try:
                client = OpenAI(api_key=self.deepseek_api_key, base_url=self.deepseek_base_url)
                response = client.chat.completions.create(
                    model=self.model,
                    messages=[{"role": "system", "content": self.last_prompt}],
                    stream=False
                )
                return response.choices[0].message.content, formatted_evidence
            except Exception as e:
                print(f"Error while calling DeepSeek API: {e}")
                raise RuntimeError("DeepSeek API call failed.") from e
        else: # openai model
            client = OpenAI(api_key=self.open_api_key)
            try:
                response = client.chat.completions.create(
                    model=self.model,
                    messages=[
                        {"role": "system", "content": self.last_prompt},
                        {"role": "user", "content": query}
                    ],
                    max_tokens=1500,
                    temperature=1.0
                )
                return response.choices[0].message.content, formatted_evidence
            except Exception as e:
                print(f"If you try to use deepseek, check your api_key. If you try to use open ai, Error while calling OpenAI API: {e}")
                raise RuntimeError("If you try to use deepseek, check your api_key. If you try to use open ai, Error while calling OpenAI API") from e


        return "DeepSeek API key not provided. Returning prompt only."

