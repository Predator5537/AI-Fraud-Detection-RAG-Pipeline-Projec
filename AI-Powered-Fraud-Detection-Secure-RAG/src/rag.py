# Simple RAG: TF-IDF + cosine similarity retrieval (prototype)
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

class SimpleRAG:
    def __init__(self):
        self.docs = []  # list of dicts with 'id' and 'text'
        self.vectorizer = None
        self.doc_matrix = None

    def ingest(self, docs):
        texts = [d['text'] for d in docs]
        if self.vectorizer is None:
            self.vectorizer = TfidfVectorizer(stop_words='english', max_features=2000)
            self.doc_matrix = self.vectorizer.fit_transform(texts)
        else:
            # naive append: refit (ok for small prototypes)
            texts_existing = [d['text'] for d in self.docs] + texts
            self.vectorizer = TfidfVectorizer(stop_words='english', max_features=2000)
            self.doc_matrix = self.vectorizer.fit_transform(texts_existing)
        self.docs.extend(docs)

    def retrieve(self, query, top_k=3):
        if not self.docs:
            return []
        q_vec = self.vectorizer.transform([query])
        sims = cosine_similarity(q_vec, self.doc_matrix)[0]
        idxs = np.argsort(sims)[::-1][:top_k]
        return [{'id': self.docs[i]['id'], 'text': self.docs[i]['text'], 'score': float(sims[i])} for i in idxs]