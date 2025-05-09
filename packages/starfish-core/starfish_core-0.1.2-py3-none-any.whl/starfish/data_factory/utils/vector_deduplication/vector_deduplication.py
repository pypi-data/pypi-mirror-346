"""
Vector-based deduplication hooks for Starfish data factory.

This module provides hooks for deduplicating generated data using vector embeddings.
It checks for similarity between generated content and existing entries in the state's
vector database, marking records as duplicates if similarity exceeds a threshold.
"""

import asyncio
import numpy as np
from typing import Dict, Any, List, Optional, Tuple, Union, Callable
import random
import threading

from starfish.common.logger import get_logger

logger = get_logger(__name__)

# Placeholder for actual embedding model - in production, use OpenAI's embedding API
async def get_embedding_mock(text: str) -> List[float]:
    """
    Mock function to generate embeddings for testing purposes.
    
    In production, replace with actual OpenAI embedding API call:
    
    ```python
    from openai import OpenAI
    client = OpenAI()
    response = client.embeddings.create(
        model="text-embedding-3-small",
        input=text
    )
    return response.data[0].embedding
    ```
    """
    # Generate a random vector with 1536 dimensions (same as OpenAI's text-embedding-3-small)
    vector = [random.uniform(-1, 1) for _ in range(1536)]
    # Normalize the vector
    norm = np.linalg.norm(vector)
    normalized_vector = [x / norm for x in vector]
    return normalized_vector

def cosine_similarity(vec1: List[float], vec2: List[float]) -> float:
    """
    Calculate cosine similarity between two vectors.
    
    Args:
        vec1: First vector
        vec2: Second vector
        
    Returns:
        Cosine similarity score (0-1)
    """
    dot_product = sum(a * b for a, b in zip(vec1, vec2))
    norm_a = sum(a * a for a in vec1) ** 0.5
    norm_b = sum(b * b for b in vec2) ** 0.5
    return dot_product / (norm_a * norm_b)

# Thread-safe mock embedding function for synchronous contexts
def sync_get_embedding_mock(text: str) -> List[float]:
    """Synchronous version of the mock embedding function."""
    # Generate a random vector with 1536 dimensions (same as OpenAI's text-embedding-3-small)
    vector = [random.uniform(-1, 1) for _ in range(1536)]
    # Normalize the vector
    norm = np.linalg.norm(vector)
    normalized_vector = [x / norm for x in vector]
    return normalized_vector

class VectorDeduplicationHook:
    """
    Hook for deduplicating data based on vector similarity.
    
    This hook computes embeddings for new records and compares them against
    existing records in the vector database. If similarity exceeds a threshold,
    the record is marked as a duplicate.
    """
    
    def __init__(
        self, 
        similarity_threshold: float = 0.95,
        embedding_func: Callable = sync_get_embedding_mock,  # Use sync version by default
        vector_db_state_key: str = "vector_db",
        content_key: str = "answer",
    ):
        """
        Initialize the deduplication hook.
        
        Args:
            similarity_threshold: Threshold above which records are considered duplicates (0-1)
            embedding_func: Function to generate embeddings from text
            vector_db_state_key: Key in the state where the vector database is stored
            content_key: Key in the record containing the content to check for duplication
        """
        self.similarity_threshold = similarity_threshold
        self.embedding_func = embedding_func
        self.vector_db_state_key = vector_db_state_key
        self.content_key = content_key
        self._lock = threading.Lock()
    
    def __call__(
        self,
        record_data: List[Dict[str, Any]],
        state: Any
    ) -> Tuple[List[Dict[str, Any]], str]:
        """
        Check records for duplicates based on vector similarity.
        
        This is a synchronous implementation that works with the existing hook system.
        
        Args:
            record_data: List of records to check for duplication
            state: Shared state object containing the vector database
            
        Returns:
            Tuple of (possibly modified records, status)
        """
        # Initialize vector database in state if it doesn't exist
        with self._lock:
            if state.get(self.vector_db_state_key) is None:
                state.set(self.vector_db_state_key, {
                    "embeddings": [],
                    "records": []
                })
            
            vector_db = state.get(self.vector_db_state_key)
            updated_records = []
            is_duplicate = False
            
            for record in record_data:
                if self.content_key not in record:
                    # Skip records that don't have the content key
                    updated_records.append(record)
                    continue
                    
                content = record[self.content_key]
                
                # Use synchronous embedding function
                embedding = self.embedding_func(content)
                
                # Check for duplicates
                duplicate_found = False
                for i, existing_embedding in enumerate(vector_db["embeddings"]):
                    similarity = cosine_similarity(embedding, existing_embedding)
                    if similarity > self.similarity_threshold:
                        duplicate_found = True
                        is_duplicate = True
                        # Add duplicate info to the record
                        record["is_duplicate"] = True
                        record["duplicate_of"] = vector_db["records"][i].get("id", i)
                        record["similarity_score"] = similarity
                        break
                
                if not duplicate_found:
                    # Add to vector database if not a duplicate
                    vector_db["embeddings"].append(embedding)
                    vector_db["records"].append(record)
                    record["is_duplicate"] = False
                
                updated_records.append(record)
            
            # Update state with new vector database
            state.set(self.vector_db_state_key, vector_db)
            
            # Return status based on whether duplicates were found
            status = "duplicate" if is_duplicate else "completed"
            return updated_records, status


# Factory function to create a deduplication hook with specified parameters
def create_deduplication_hook(
    similarity_threshold: float = 0.95,
    embedding_func: Callable = sync_get_embedding_mock,  # Use sync version by default
    vector_db_state_key: str = "vector_db",
    content_key: str = "answer"
) -> VectorDeduplicationHook:
    """
    Create a deduplication hook with the specified parameters.
    
    Args:
        similarity_threshold: Threshold above which records are considered duplicates (0-1)
        embedding_func: Function to generate embeddings from text
        vector_db_state_key: Key in the state where the vector database is stored
        content_key: Key in the record containing the content to check for duplication
        
    Returns:
        Configured VectorDeduplicationHook instance
    """
    return VectorDeduplicationHook(
        similarity_threshold=similarity_threshold,
        embedding_func=embedding_func,
        vector_db_state_key=vector_db_state_key,
        content_key=content_key
    ) 