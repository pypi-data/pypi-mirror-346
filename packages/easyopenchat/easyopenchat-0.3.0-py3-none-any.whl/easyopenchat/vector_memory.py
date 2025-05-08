
# # Placeholder for vector memory (e.g., for embeddings)
# # Can integrate FAISS, ChromaDB, etc.

# class VectorMemory:
#     def __init__(self):
#         self.vectors = []  # Dummy placeholder

#     def add(self, embedding, metadata):
#         self.vectors.append((embedding, metadata))

#     def search(self, query_embedding):
#         return "Not implemented"





try:
    import faiss
    import numpy as np
    FAISS_AVAILABLE = True
except ImportError:
    FAISS_AVAILABLE = False

class VectorMemory:
    def __init__(self, dimension=384):
        """
        Initialize vector memory for semantic search.
        
        Args:
            dimension (int): Dimension of embeddings (default: 384 for small models).
        """
        if not FAISS_AVAILABLE:
            raise ImportError("FAISS is not installed. Install with 'pip install faiss-cpu' or enable vector memory.")
        self.dimension = dimension
        self.index = faiss.IndexFlatL2(dimension)
        self.metadata = []

    def add(self, embedding, metadata):
        """
        Add an embedding with metadata.
        
        Args:
            embedding (list or np.array): Embedding vector.
            metadata (dict): Associated metadata.
        """
        embedding = np.array(embedding, dtype=np.float32).reshape(1, -1)
        self.index.add(embedding)
        self.metadata.append(metadata)

    def search(self, query_embedding, k=5):
        """
        Search for k nearest embeddings.
        
        Args:
            query_embedding (list or np.array): Query embedding.
            k (int): Number of results to return.
        
        Returns:
            list: List of (distance, metadata) tuples.
        """
        query_embedding = np.array(query_embedding, dtype=np.float32).reshape(1, -1)
        distances, indices = self.index.search(query_embedding, k)
        return [(distances[0][i], self.metadata[indices[0][i]]) for i in range(len(indices[0]))]