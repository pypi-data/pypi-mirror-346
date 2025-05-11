"""
Media handling components for AI-on-Rails.

This package provides models and handlers for working with various media types.
"""

from .models import (
    MediaType,
    MediaFormat,
    MediaItem,
    TextItem,
    ImageItem,
    AudioItem,
    VideoItem,
    Model3DItem,
    DocumentItem,
    BinaryItem,
    MediaItemUnion
)

from .handlers import (
    MediaHandler,
    TextHandler,
    ImageHandler,
    AudioHandler,
    MediaHandlerRegistry,
    media_registry
)

__all__ = [
    # Models
    "MediaType",
    "MediaFormat",
    "MediaItem",
    "TextItem",
    "ImageItem",
    "AudioItem",
    "VideoItem", 
    "Model3DItem",
    "DocumentItem",
    "BinaryItem",
    "MediaItemUnion",
    
    # Handlers
    "MediaHandler",
    "TextHandler",
    "ImageHandler",
    "AudioHandler",
    "MediaHandlerRegistry",
    "media_registry"
]