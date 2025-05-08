import os
from dotenv import load_dotenv
from .embedding import Embedding
from .retriever import Retriever
from .index import IndexManager # faiss index 이걸로 관리하자
from .agent import Agent

class RagService:
    def __init__(
            self,
            embedding_model="text-embedding-3-small",
            response_model="deepseek-chat",
            open_api_key=None,
            deepseek_api_key=None,
            deepseek_base_url="https://api.deepseek.com",
            context_expansion=False,
            expansion_window=1
    ):
        load_dotenv()

        # set keys
        self.open_api_key = open_api_key or os.getenv("OPENAI_API_KEY")
        self.deepseek_api_key = deepseek_api_key or os.getenv("DEEPSEEK_API_KEY")
        self.deepseek_base_url = deepseek_base_url

        # init module
        self.index_manager = IndexManager()
        self.embedding = Embedding(api_key=self.open_api_key, model=embedding_model)
        self.retriever = Retriever(self.embedding)
        self.agent = Agent(
            model=response_model,
            embedding_model=embedding_model,
            open_api_key=self.open_api_key,
            deepseek_api_key=self.deepseek_api_key,
            deepseek_base_url=self.deepseek_base_url,
        )

        # Set initial context expansion settings
        self.set_context_expansion(context_expansion, expansion_window)

        # validation
        self.validate_configuration()
    
    def validate_configuration(self):
        if not self.open_api_key:
            raise ValueError("OPEN_API_KEY is required")
        if self.agent.model == "deepseek-chat" and not self.deepseek_api_key:
            raise ValueError("DEEPSEEK_API_KEY is required for deepseek-chat model")
    
    """
    def rsc(self, resource_path, index_file="faiss_index.bin", metadata_file="metadata.json", force_update=False, max_workers=10):
        ###리소스 로드하고 임베딩 생성해야해. 
        ## 패스 아래의 모든 자료를 읽되, 메타데이터에서 이들 자료를 구분해야해
        ## max_workers 자율 조정을 위한 파라미터 추가. v1.0.13
        ## resource_path+{"Index"} 아래로 파일들 저장해야해. 
        if not force_update:
            index, metadata = self.index_manager.load(index_file, metadata_file)
            if index and metadata:
                return index, metadata

        index, metadata = self.retriever.load_resources(resource_path, max_workers=max_workers)
        self.index_manager.save(index, metadata, index_file, metadata_file)
        return index, metadata
    """

    def rsc(self, resource_path, index_file="faiss_index.bin", metadata_file="metadata.json", force_update=False, chunkers=10, embedders=10, ef_construction=200, ef_search=100, M=48):
        ### Resource loading and embedding generation
        if not force_update:
            index, metadata = self.index_manager.load(resource_path, index_file, metadata_file)
            if index and metadata:
                return index, metadata

        index, metadata = self.retriever.load_resources(resource_path, chunkers=chunkers, embedders=embedders, ef_construction=ef_construction, ef_search=ef_search, M=M)
        self.index_manager.save(index, metadata, resource_path, index_file, metadata_file)
        return index, metadata
    
    def set_context_expansion(self, enable: bool, window_size: int = 1):
        """컨텍스트 확장 설정을 변경합니다.
        
        Args:
            enable (bool): 컨텍스트 확장 기능 활성화 여부
            window_size (int): 앞뒤로 포함할 청크의 수
        """
        self.agent.set_context_expansion(enable, window_size)

    def generate_response(self, resource, query, evidence_num=3, context_expansion=None, expansion_window=None):
        """응답을 생성합니다.
        
        Args:
            resource: 리소스 (인덱스와 메타데이터)
            query (str): 사용자 질의
            evidence_num (int): 검색할 증거 문서 수
            context_expansion (bool, optional): 컨텍스트 확장 사용 여부. None이면 현재 설정 유지
            expansion_window (int, optional): 확장할 컨텍스트 윈도우 크기. None이면 현재 설정 유지
        
        Returns:
            tuple: (생성된 응답, 사용된 증거)
        """
        if context_expansion is not None:
            self.set_context_expansion(context_expansion, expansion_window or 1)
            
        response, top_evidence = self.agent.generate_response(resource, query, evidence_num=evidence_num)
        return response, top_evidence