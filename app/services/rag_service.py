import re
import sys
from typing import List

from langchain_google_genai import GoogleGenerativeAIEmbeddings

try:
    from langchain_community.vectorstores import FAISS, Chroma
except Exception:
    FAISS = None
    Chroma = None


def get_embeddings():
    return GoogleGenerativeAIEmbeddings(model="models/embedding-001")


def create_vector_db(texts: List[str]):
    if sys.platform == "darwin" and Chroma is not None:
        embeddings = get_embeddings()
        return Chroma.from_texts(texts, embeddings)
    if FAISS is not None:
        embeddings = get_embeddings()
        return FAISS.from_texts(texts, embeddings)
    return SimpleVectorDB(texts)


class SimpleDoc:
    def __init__(self, text: str):
        self.page_content = text


class SimpleVectorDB:
    def __init__(self, texts: List[str]):
        self.texts = texts

    def similarity_search(self, query: str, k: int = 2) -> List[SimpleDoc]:
        tokens = set(re.findall(r"\w+", query.lower()))
        scored = []
        for text in self.texts:
            lowered = text.lower()
            score = sum(1 for token in tokens if token in lowered)
            scored.append((score, text))
        scored.sort(key=lambda item: item[0], reverse=True)
        return [SimpleDoc(text) for _, text in scored[:k]]


# Default docs from the notebook
DEFAULT_DOCS = [
    "Delivery delays are usually resolved within 48 hours.",
    "Refund requests are processed within 5 business days.",
    "Escalate negative sentiment cases to senior support.",
]


class RAGService:
    def __init__(self, docs: List[str] = DEFAULT_DOCS):
        self.vector_db = create_vector_db(docs)

    def search(self, query: str, k: int = 2) -> List[str]:
        results = self.vector_db.similarity_search(query, k=k)
        return [r.page_content for r in results]
