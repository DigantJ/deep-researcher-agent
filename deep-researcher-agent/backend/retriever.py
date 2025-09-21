import os, json, numpy as np
from sentence_transformers import SentenceTransformer
try:
    import faiss
except Exception:
    faiss = None
import pathlib

class Retriever:
    def __init__(self, index_path='data/faiss_index', store_path='data/docs.jsonl'):
        self.index_path = index_path
        self.store_path = store_path
        os.makedirs(os.path.dirname(self.index_path), exist_ok=True)
        self.model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')
        self.dim = self.model.get_sentence_embedding_dimension()
        self.index = None
        self.docs = []
        self._load()

    def _load(self):
        # load docs if exists
        if os.path.exists(self.store_path):
            with open(self.store_path, 'r', encoding='utf-8') as f:
                self.docs = [json.loads(line) for line in f]
        # create index
        if faiss is not None and os.path.exists(self.index_path):
            try:
                self.index = faiss.read_index(self.index_path)
            except Exception:
                self.index = None

    def add_documents(self, docs):
        # docs: list of {"id":..., "title":..., "text":...}
        new = []
        for d in docs:
            if 'id' not in d:
                d['id'] = str(len(self.docs)+len(new)+1)
            new.append(d)
        # append to store file
        with open(self.store_path, 'a', encoding='utf-8') as f:
            for d in new:
                f.write(json.dumps(d, ensure_ascii=False) + '\n')
        self.docs.extend(new)
        # build or update FAISS
        texts = [d.get('text','') for d in self.docs]
        embeddings = self.model.encode(texts, show_progress_bar=False, convert_to_numpy=True)
        if faiss is not None:
            import faiss as _faiss
            if self.index is None:
                self.index = _faiss.IndexFlatIP(self.dim)
            # normalize for cosine
            _faiss.normalize_L2(embeddings)
            # rebuild index (simple approach)
            self.index.reset()
            self.index.add(embeddings)
            _faiss.write_index(self.index, self.index_path)
        else:
            # fallback: store embeddings in-memory (not persistent)
            self._embeddings = embeddings

    def get_relevant(self, query, top_k=4):
        q_emb = self.model.encode([query], convert_to_numpy=True)
        if faiss is not None and self.index is not None:
            import faiss as _faiss
            _faiss.normalize_L2(q_emb)
            D, I = self.index.search(q_emb, top_k)
            results = []
            for idx in I[0]:
                if idx < len(self.docs):
                    results.append(self.docs[idx])
            return results
        else:
            # naive cosine similarity fallback
            from numpy import dot
            from numpy.linalg import norm
            sims = []
            for emb, doc in zip(self._embeddings, self.docs):
                sim = dot(q_emb[0], emb)/(norm(q_emb[0])*norm(emb)+1e-9)
                sims.append(sim)
            idxs = sorted(range(len(sims)), key=lambda i: sims[i], reverse=True)[:top_k]
            return [self.docs[i] for i in idxs]
