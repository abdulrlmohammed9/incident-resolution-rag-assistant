import numpy as np
from sentence_transformers import SentenceTransformer

from chunking import chunk_runbook
from ingest import load_runbooks


class RunbookRetriever:
    def __init__(self, chunks):
        if not chunks:
            raise ValueError("No runbook passages found. Run src/chunking.py first.")

        self.chunks = chunks
        self.model = SentenceTransformer(
            "sentence-transformers/all-MiniLM-L6-v2"
        )
        self.embeddings = self.model.encode(
            [chunk["text"] for chunk in chunks],
            normalize_embeddings=True,
        )

    def search(self, question, top_k=3):
        question_vector = self.model.encode(
            question,
            normalize_embeddings=True,
        )

        # The dot product of normalized vectors gives cosine similarity.
        scores = self.embeddings @ question_vector
        ranked_indices = np.argsort(-scores)[:top_k]

        return [
            (self.chunks[index], float(scores[index]))
            for index in ranked_indices
        ]


if __name__ == "__main__":
    chunks = [
        chunk
        for runbook in load_runbooks()
        for chunk in chunk_runbook(runbook)
    ]
    retriever = RunbookRetriever(chunks)

    questions = [
        "The server rejected my SSH key. What should I check?",
        "The connection times out before login. How do I check whether the port is reachable?",
    ]

    for question in questions:
        print(f"\nQuestion: {question}")

        for rank, (chunk, score) in enumerate(retriever.search(question, top_k=8), start=1):
            print(f"[{rank}] {chunk['source']} | {chunk['section']} | {score:.3f}")