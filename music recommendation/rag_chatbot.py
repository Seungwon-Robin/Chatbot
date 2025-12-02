import yaml
import pandas as pd
import numpy as np
import faiss
import google.generativeai as genai
import os
from sentence_transformers import SentenceTransformer
import torch

class RAGChatbot:
    def __init__(self, config_path='config.yaml', db_path='music_db.csv', index_path='faiss_index.bin'):
        """
        챗봇 초기화
        - 설정 파일 로드 (API 키, 모델 이름)
        - GenAI 및 임베딩 모델 설정
        - 데이터베이스 로드 및 RAG 파이p라인 설정
        """
        with open(config_path, 'r') as f:
            config = yaml.safe_load(f)

        self.api_key = config['api_key']
        self.model_name = config['model_name']
        
        # GenAI 설정 (답변 생성용)
        genai.configure(api_key=self.api_key)
        
        # 디바이스 설정 (GPU 사용 가능 여부 확인)
        self.device = 'cuda' if torch.cuda.is_available() else 'cpu'
        print(f"Using device: {self.device}")

        # 문장 임베딩 모델 설정 (무료 모델)
        self.embedding_model = SentenceTransformer('jhgan/ko-sroberta-multitask', device=self.device)
        
        self.db = pd.read_csv(db_path)
        self.index_path = index_path
        
        self._setup_rag_pipeline()

    def _embed_text(self, text: str) -> np.ndarray:
        """텍스트를 임베딩 벡터로 변환"""
        # 단일 텍스트 임베딩
        embedding = self.embedding_model.encode(text, convert_to_numpy=True)
        return embedding

    def _setup_rag_pipeline(self):
        """
        RAG 파이프라인 설정
        - 저장된 인덱스가 있으면 로드, 없으면 생성 후 저장
        """
        if os.path.exists(self.index_path):
            print("저장된 인덱스를 불러옵니다...")
            self.index = faiss.read_index(self.index_path)
            print("인덱스 로드 완료.")
        else:
            print("새로운 인덱스를 생성합니다... (시간이 걸릴 수 있습니다)")
            descriptions = self.db['description'].tolist()
            
            try:
                # Sentence Transformer를 사용하여 문서 임베딩 생성
                print("문서 임베딩 중...")
                embeddings = self.embedding_model.encode(descriptions, convert_to_numpy=True, show_progress_bar=True)
                
                # FAISS 인덱스 생성 및 저장
                print("FAISS 인덱스 생성 중...")
                self.index = faiss.IndexFlatL2(embeddings.shape[1])
                self.index.add(embeddings.astype('float32'))
                
                print("인덱스를 파일로 저장합니다...")
                faiss.write_index(self.index, self.index_path)
                print("인덱스 생성 및 저장 완료.")

            except Exception as e:
                print(f"임베딩 또는 인덱스 생성 중 오류가 발생했습니다: {e}")
                exit() # 오류 발생 시 프로그램 종료

    def _search(self, query: str, k: int = 3) -> pd.DataFrame:
        """FAISS 인덱스에서 유사한 문서를 검색"""
        query_embedding = self._embed_text(query)
        query_embedding = np.expand_dims(query_embedding, axis=0).astype('float32')
        
        distances, indices = self.index.search(query_embedding, k)
        
        return self.db.iloc[indices[0]]

    def generate_response(self, query: str) -> str:
        """
        RAG를 통해 사용자 질문에 대한 답변 생성
        """
        retrieved_data = self._search(query)
        
        context = ""
        for _, row in retrieved_data.iterrows():
            context += f"- 장르: {row['genre']}, 아티스트: {row['artist']}, 제목: {row['song_title']}\n  설명: {row['description']}\n"

        prompt = f'''
        당신은 사용자의 기분이나 상황에 맞는 노래를 추천해주는 음악 전문가입니다.
        아래의 검색된 노래 정보를 바탕으로 사용자의 질문에 가장 적절한 노래를 추천해주세요.
        추천할 때는 왜 이 노래를 추천하는지 간단한 이유를 함께 설명해주세요.

        [사용자 질문]
        {query}

        [검색된 노래 정보]
        {context}

        [답변]
        '''
        
        model = genai.GenerativeModel(self.model_name)
        response = model.generate_content(prompt)
        
        return response.text


