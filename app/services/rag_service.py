import re
import sys
import os
import logging
from typing import List

from dotenv import load_dotenv
from langchain_google_genai import GoogleGenerativeAIEmbeddings

try:
    from langchain_community.vectorstores import FAISS, Chroma
except Exception:
    FAISS = None
    Chroma = None

load_dotenv()
LOGGER = logging.getLogger(__name__)
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "models/gemini-embedding-001")


def get_embeddings():
    return GoogleGenerativeAIEmbeddings(model=EMBEDDING_MODEL)


def create_vector_db(texts: List[str]):
    try:
        if sys.platform == "darwin" and Chroma is not None:
            embeddings = get_embeddings()
            return Chroma.from_texts(texts, embeddings)
        if FAISS is not None:
            embeddings = get_embeddings()
            return FAISS.from_texts(texts, embeddings)
    except Exception as exc:
        LOGGER.warning(
            "Vector DB initialization failed for model '%s': %s. Falling back to SimpleVectorDB.",
            EMBEDDING_MODEL,
            exc,
        )
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
        self.docs = docs
        self.vector_db = create_vector_db(docs)

    def search(self, query: str, k: int = 2) -> List[str]:
        try:
            results = self.vector_db.similarity_search(query, k=k)
        except Exception as exc:
            LOGGER.warning(
                "Vector search failed: %s. Reverting to SimpleVectorDB for this runtime.",
                exc,
            )
            self.vector_db = SimpleVectorDB(self.docs)
            results = self.vector_db.similarity_search(query, k=k)
        return [r.page_content for r in results]
