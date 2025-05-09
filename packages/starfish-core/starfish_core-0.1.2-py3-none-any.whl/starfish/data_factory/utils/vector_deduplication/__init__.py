"""
Vector deduplication hooks for Starfish data factory.
"""

from .vector_deduplication import (
    VectorDeduplicationHook,
    create_deduplication_hook,
    get_embedding_mock,
    sync_get_embedding_mock,
    cosine_similarity
)

__all__ = [
    "VectorDeduplicationHook",
    "create_deduplication_hook",
    "get_embedding_mock",
    "sync_get_embedding_mock",
    "cosine_similarity"
] 