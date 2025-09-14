"""Placeholder for vector database interactions."""

class VectorDB:
    """Minimal interface to a vector database."""

    def __init__(self):
        self._store = {}

    def add(self, key: str, embedding: list[float]):
        self._store[key] = embedding

    def similarity(self, query: list[float]):
        # naive cosine similarity
        import math

        def cos(a, b):
            dot = sum(x * y for x, y in zip(a, b))
            norm_a = math.sqrt(sum(x * x for x in a))
            norm_b = math.sqrt(sum(x * x for x in b))
            return dot / (norm_a * norm_b)

        return sorted(
            ((key, cos(embedding, query)) for key, embedding in self._store.items()),
            key=lambda x: x[1],
            reverse=True,
        )
