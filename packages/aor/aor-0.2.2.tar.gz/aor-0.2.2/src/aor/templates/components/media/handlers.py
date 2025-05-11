"""
Media handlers for AI-on-Rails.

This module provides handlers for different media types,
including validation, conversion, and processing functionality.
"""

import base64
import mimetypes
import hashlib
import re
from typing import Dict, Any, Optional, List, Tuple
from pathlib import Path
import json
import io
from abc import ABC, abstractmethod

from .models import (
    MediaType, MediaFormat, MediaItem, TextItem, ImageItem, 
    AudioItem, VideoItem, Model3DItem, DocumentItem, BinaryItem
)


class MediaHandler(ABC):
    """Base class for all media handlers."""
    
    @abstractmethod
    def validate(self, item: MediaItem) -> Tuple[bool, Optional[str]]:
        """
        Validate a media item.
        
        Returns:
            Tuple of (is_valid, error_message)
        """
        pass
    
    @abstractmethod
    def process(self, item: MediaItem) -> MediaItem:
        """
        Process a media item (e.g., normalize, convert format).
        
        Returns:
            Processed media item
        """
        pass
    
    @abstractmethod
    def get_metadata(self, item: MediaItem) -> Dict[str, Any]:
        """
        Extract metadata from a media item.
        
        Returns:
            Dictionary of metadata
        """
        pass


class TextHandler(MediaHandler):
    """Handler for text media."""
    
    MAX_TEXT_LENGTH = 1_000_000  # 1 million characters
    
    def validate(self, item: TextItem) -> Tuple[bool, Optional[str]]:
        if not isinstance(item, TextItem):
            return False, "Item must be a TextItem instance"
        
        if not item.content:
            return False, "Text content cannot be empty"
        
        if len(item.content) > self.MAX_TEXT_LENGTH:
            return False, f"Text content exceeds maximum length of {self.MAX_TEXT_LENGTH} characters"
        
        if item.format not in [MediaFormat.PLAIN, MediaFormat.MARKDOWN, MediaFormat.HTML, 
                              MediaFormat.JSON, MediaFormat.XML, MediaFormat.CSV]:
            return False, f"Unsupported text format: {item.format}"
        
        return True, None
    
    def process(self, item: TextItem) -> TextItem:
        # Normalize line endings
        if item.format == MediaFormat.PLAIN:
            item.content = item.content.replace('\r\n', '\n').replace('\r', '\n')
        
        # Auto-detect format if not specified
        if not item.format:
            item.format = self._detect_format(item.content)
        
        return item
    
    def get_metadata(self, item: TextItem) -> Dict[str, Any]:
        metadata = {
            "length": len(item.content),
            "lines": item.content.count('\n') + 1,
            "format": item.format,
            "word_count": len(item.content.split()),
            "hash": hashlib.md5(item.content.encode()).hexdigest()
        }
        
        # Add format-specific metadata
        if item.format == MediaFormat.JSON:
            try:
                json_data = json.loads(item.content)
                metadata["json_structure"] = self._analyze_json_structure(json_data)
            except json.JSONDecodeError:
                metadata["json_valid"] = False
        
        return metadata
    
    def _detect_format(self, content: str) -> str:
        """Auto-detect text format based on content."""
        if self._is_json(content):
            return MediaFormat.JSON
        elif self._is_html(content):
            return MediaFormat.HTML
        elif self._is_markdown(content):
            return MediaFormat.MARKDOWN
        elif self._is_xml(content):
            return MediaFormat.XML
        elif self._is_csv(content):
            return MediaFormat.CSV
        else:
            return MediaFormat.PLAIN
    
    def _is_json(self, content: str) -> bool:
        try:
            json.loads(content)
            return True
        except:
            return False
    
    def _is_html(self, content: str) -> bool:
        return bool(re.search(r'<\s*html[^>]*>', content, re.IGNORECASE))
    
    def _is_markdown(self, content: str) -> bool:
        markdown_patterns = [
            r'^#{1,6}\s',  # Headers
            r'\[.*?\]\(.*?\)',  # Links
            r'```.*?```',  # Code blocks
            r'\*\*.+?\*\*',  # Bold
            r'__.+?__'  # Bold alternative
        ]
        return any(re.search(pattern, content, re.MULTILINE) for pattern in markdown_patterns)
    
    def _is_xml(self, content: str) -> bool:
        return content.strip().startswith('<?xml')
    
    def _is_csv(self, content: str) -> bool:
        lines = content.strip().split('\n')
        if len(lines) < 2:
            return False
        delimiters = [',', ';', '\t', '|']
        for delimiter in delimiters:
            fields_per_line = [len(line.split(delimiter)) for line in lines[:5]]
            if len(set(fields_per_line)) == 1 and fields_per_line[0] > 1:
                return True
        return False
    
    def _analyze_json_structure(self, data: Any) -> Dict[str, Any]:
        """Analyze JSON structure for metadata."""
        if isinstance(data, dict):
            return {"type": "object", "keys": list(data.keys())}
        elif isinstance(data, list):
            return {"type": "array", "length": len(data)}
        else:
            return {"type": type(data).__name__}


class ImageHandler(MediaHandler):
    """Handler for image media."""
    
    MAX_IMAGE_SIZE = 10 * 1024 * 1024  # 10MB
    SUPPORTED_FORMATS = [MediaFormat.JPG, MediaFormat.JPEG, MediaFormat.PNG, 
                        MediaFormat.GIF, MediaFormat.SVG, MediaFormat.WEBP]
    
    def validate(self, item: ImageItem) -> Tuple[bool, Optional[str]]:
        if not isinstance(item, ImageItem):
            return False, "Item must be an ImageItem instance"
        
        if not item.url and not item.base64_content:
            return False, "Image must have either URL or base64 content"
        
        if item.format and item.format not in self.SUPPORTED_FORMATS:
            return False, f"Unsupported image format: {item.format}"
        
        if item.base64_content:
            try:
                data = base64.b64decode(item.base64_content)
                if len(data) > self.MAX_IMAGE_SIZE:
                    return False, f"Image exceeds maximum size of {self.MAX_IMAGE_SIZE} bytes"
            except Exception as e:
                return False, f"Invalid base64 content: {str(e)}"
        
        return True, None
    
    def process(self, item: ImageItem) -> ImageItem:
        # Auto-detect format if not specified
        if not item.format and item.base64_content:
            item.format = self._detect_format_from_base64(item.base64_content)
        
        # Ensure alt text exists
        if not item.alt_text and item.metadata.get("description"):
            item.alt_text = item.metadata["description"]
        
        return item
    
    def get_metadata(self, item: ImageItem) -> Dict[str, Any]:
        metadata = {
            "format": item.format,
            "has_url": bool(item.url),
            "has_base64": bool(item.base64_content)
        }
        
        if item.width:
            metadata["width"] = item.width
        if item.height:
            metadata["height"] = item.height
        
        if item.base64_content:
            data = base64.b64decode(item.base64_content)
            metadata["size_bytes"] = len(data)
            metadata["hash"] = hashlib.md5(data).hexdigest()
        
        return metadata
    
    def _detect_format_from_base64(self, base64_content: str) -> str:
        """Detect image format from base64 content."""
        try:
            data = base64.b64decode(base64_content)
            
            # Check magic numbers
            if data.startswith(b'\xFF\xD8\xFF'):
                return MediaFormat.JPEG
            elif data.startswith(b'\x89PNG\r\n\x1a\n'):
                return MediaFormat.PNG
            elif data.startswith(b'GIF87a') or data.startswith(b'GIF89a'):
                return MediaFormat.GIF
            elif data.startswith(b'<svg'):
                return MediaFormat.SVG
            elif data.startswith(b'RIFF') and data[8:12] == b'WEBP':
                return MediaFormat.WEBP
            else:
                return MediaFormat.BINARY
        except:
            return MediaFormat.BINARY


class AudioHandler(MediaHandler):
    """Handler for audio media."""
    
    MAX_AUDIO_SIZE = 50 * 1024 * 1024  # 50MB
    SUPPORTED_FORMATS = [MediaFormat.MP3, MediaFormat.WAV, MediaFormat.OGG, MediaFormat.FLAC]
    
    def validate(self, item: AudioItem) -> Tuple[bool, Optional[str]]:
        if not isinstance(item, AudioItem):
            return False, "Item must be an AudioItem instance"
        
        if not item.url and not item.base64_content:
            return False, "Audio must have either URL or base64 content"
        
        if item.format and item.format not in self.SUPPORTED_FORMATS:
            return False, f"Unsupported audio format: {item.format}"
        
        return True, None
    
    def process(self, item: AudioItem) -> AudioItem:
        return item
    
    def get_metadata(self, item: AudioItem) -> Dict[str, Any]:
        metadata = {
            "format": item.format,
            "has_url": bool(item.url),
            "has_base64": bool(item.base64_content),
            "has_transcript": bool(item.transcript)
        }
        
        if item.duration_seconds:
            metadata["duration_seconds"] = item.duration_seconds
        
        return metadata


class MediaHandlerRegistry:
    """Registry for media handlers."""
    
    def __init__(self):
        self._handlers = {
            MediaType.TEXT: TextHandler(),
            MediaType.IMAGE: ImageHandler(),
            MediaType.AUDIO: AudioHandler(),
            # Add more handlers as needed
        }
    
    def get_handler(self, media_type: MediaType) -> Optional[MediaHandler]:
        """Get handler for media type."""
        return self._handlers.get(media_type)
    
    def register_handler(self, media_type: MediaType, handler: MediaHandler):
        """Register a new handler."""
        self._handlers[media_type] = handler
    
    def validate_item(self, item: MediaItem) -> Tuple[bool, Optional[str]]:
        """Validate a media item using the appropriate handler."""
        handler = self.get_handler(item.media_type)
        if handler:
            return handler.validate(item)
        return False, f"No handler for media type: {item.media_type}"
    
    def process_item(self, item: MediaItem) -> MediaItem:
        """Process a media item using the appropriate handler."""
        handler = self.get_handler(item.media_type)
        if handler:
            return handler.process(item)
        return item
    
    def get_item_metadata(self, item: MediaItem) -> Dict[str, Any]:
        """Get metadata for a media item."""
        handler = self.get_handler(item.media_type)
        if handler:
            return handler.get_metadata(item)
        return {}


# Singleton registry instance
media_registry = MediaHandlerRegistry()