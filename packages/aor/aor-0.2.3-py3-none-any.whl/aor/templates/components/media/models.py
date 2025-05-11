"""
Media models for AI-on-Rails.

This module defines standard models for working with various media types
including text, images, audio, video, documents, and more.
"""

from typing import Dict, List, Optional, Union, Any, Literal
from pydantic import BaseModel, Field, HttpUrl
from enum import Enum
from datetime import datetime


class MediaType(str, Enum):
    """Defines the media type for inputs and outputs."""
    TEXT = "text"
    IMAGE = "image"
    AUDIO = "audio"
    VIDEO = "video"
    MODEL_3D = "3d_model"
    PDF = "pdf"
    DOCUMENT = "document"
    SPREADSHEET = "spreadsheet"
    BINARY = "binary"
    JSON = "json"
    MARKDOWN = "markdown"
    HTML = "html"
    CSV_TEXT = "csv"
    XML = "xml"
    CUSTOM = "custom"


class MediaFormat(str, Enum):
    """Common formats for different media types."""
    # Text formats
    PLAIN = "plain"
    MARKDOWN = "markdown"
    HTML = "html"
    JSON = "json"
    XML = "xml"
    CSV = "csv"
    
    # Image formats
    JPG = "jpg"
    JPEG = "jpeg"
    PNG = "png"
    GIF = "gif"
    SVG = "svg"
    WEBP = "webp"
    
    # Audio formats
    MP3 = "mp3"
    WAV = "wav"
    OGG = "ogg"
    FLAC = "flac"
    
    # Video formats
    MP4 = "mp4"
    AVI = "avi"
    MOV = "mov"
    WEBM = "webm"
    
    # 3D model formats
    OBJ = "obj"
    GLB = "glb"
    GLTF = "gltf"
    FBX = "fbx"
    
    # Document formats
    PDF = "pdf"
    DOCX = "docx"
    TXT = "txt"
    
    # Spreadsheet formats
    XLSX = "xlsx"
    CSV_SPREADSHEET = "csv"
    
    # Other
    BINARY = "binary"
    CUSTOM = "custom"


class MediaItem(BaseModel):
    """
    Base class for all media items.
    Used as part of lists in structured inputs and outputs.
    """
    media_type: MediaType = Field(..., description="Type of media content")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Additional metadata about this media item")
    timestamp: Optional[datetime] = Field(default_factory=datetime.now, description="When the item was created or processed")
    
    class Config:
        json_schema_extra = {
            "example": {
                "media_type": "text",
                "metadata": {"source": "user", "language": "en"},
                "timestamp": "2024-04-20T12:34:56.789Z"
            }
        }


class TextItem(MediaItem):
    """Text media item."""
    media_type: MediaType = Field(MediaType.TEXT, const=True)
    content: str = Field(..., description="The text content")
    format: Optional[str] = Field(
        MediaFormat.PLAIN, description="Format of the text content"
    )


class ImageItem(MediaItem):
    """Image media item."""
    media_type: MediaType = Field(MediaType.IMAGE, const=True)
    url: Optional[HttpUrl] = Field(None, description="URL to the image content")
    base64_content: Optional[str] = Field(None, description="Base64 encoded image content")
    format: Optional[str] = Field(None, description="Format/extension of the image (jpg, png, etc.)")
    width: Optional[int] = Field(None, description="Width of the image in pixels")
    height: Optional[int] = Field(None, description="Height of the image in pixels")
    alt_text: Optional[str] = Field(None, description="Alternative text describing the image")
    
    class Config:
        json_schema_extra = {
            "example": {
                "media_type": "image",
                "url": "https://example.com/image.jpg",
                "format": "jpg",
                "width": 1200,
                "height": 800,
                "alt_text": "A scenic mountain landscape",
                "metadata": {"source": "user_upload", "size_bytes": 256000}
            }
        }


class AudioItem(MediaItem):
    """Audio media item."""
    media_type: MediaType = Field(MediaType.AUDIO, const=True)
    url: Optional[HttpUrl] = Field(None, description="URL to the audio content")
    base64_content: Optional[str] = Field(None, description="Base64 encoded audio content")
    format: Optional[str] = Field(None, description="Format/extension of the audio (mp3, wav, etc.)")
    duration_seconds: Optional[float] = Field(None, description="Duration of the audio in seconds")
    transcript: Optional[str] = Field(None, description="Text transcript of the audio content")
    
    class Config:
        json_schema_extra = {
            "example": {
                "media_type": "audio",
                "url": "https://example.com/audio.mp3",
                "format": "mp3",
                "duration_seconds": 120.5,
                "transcript": "This is a transcript of the audio...",
                "metadata": {"bitrate": "320kbps", "channels": 2}
            }
        }


class VideoItem(MediaItem):
    """Video media item."""
    media_type: MediaType = Field(MediaType.VIDEO, const=True)
    url: Optional[HttpUrl] = Field(None, description="URL to the video content")
    base64_content: Optional[str] = Field(None, description="Base64 encoded video content")
    format: Optional[str] = Field(None, description="Format/extension of the video (mp4, avi, etc.)")
    width: Optional[int] = Field(None, description="Width of the video in pixels")
    height: Optional[int] = Field(None, description="Height of the video in pixels")
    duration_seconds: Optional[float] = Field(None, description="Duration of the video in seconds")
    transcript: Optional[str] = Field(None, description="Text transcript of the video content")
    
    class Config:
        json_schema_extra = {
            "example": {
                "media_type": "video",
                "url": "https://example.com/video.mp4",
                "format": "mp4",
                "width": 1920,
                "height": 1080,
                "duration_seconds": 300.0,
                "metadata": {"fps": 30, "codec": "h264"}
            }
        }


class Model3DItem(MediaItem):
    """3D model media item."""
    media_type: MediaType = Field(MediaType.MODEL_3D, const=True)
    url: Optional[HttpUrl] = Field(None, description="URL to the 3D model content")
    base64_content: Optional[str] = Field(None, description="Base64 encoded model content")
    format: Optional[str] = Field(None, description="Format/extension of the 3D model (obj, gltf, fbx, etc.)")
    description: Optional[str] = Field(None, description="Description of the 3D model")
    
    class Config:
        json_schema_extra = {
            "example": {
                "media_type": "3d_model",
                "url": "https://example.com/model.glb",
                "format": "glb",
                "description": "3D model of a building",
                "metadata": {"vertices": 12500, "triangles": 22340}
            }
        }


class DocumentItem(MediaItem):
    """Document media item (PDF, DOCX, etc.)."""
    media_type: MediaType = Field(MediaType.DOCUMENT, const=True)
    url: Optional[HttpUrl] = Field(None, description="URL to the document content")
    base64_content: Optional[str] = Field(None, description="Base64 encoded document content")
    format: Optional[str] = Field(None, description="Format/extension of the document (pdf, docx, etc.)")
    text_content: Optional[str] = Field(None, description="Extracted text content from the document")
    
    class Config:
        json_schema_extra = {
            "example": {
                "media_type": "document",
                "url": "https://example.com/document.pdf",
                "format": "pdf",
                "text_content": "Extracted text from the PDF...",
                "metadata": {"pages": 5, "title": "Annual Report"}
            }
        }


class BinaryItem(MediaItem):
    """Binary data media item for other file types."""
    media_type: MediaType = Field(MediaType.BINARY, const=True)
    url: Optional[HttpUrl] = Field(None, description="URL to the binary content")
    base64_content: Optional[str] = Field(None, description="Base64 encoded binary content")
    format: Optional[str] = Field(None, description="Format/extension or MIME type of the binary content")
    description: Optional[str] = Field(None, description="Description of the binary content")
    
    class Config:
        json_schema_extra = {
            "example": {
                "media_type": "binary",
                "url": "https://example.com/data.bin",
                "format": "application/octet-stream",
                "description": "Binary data file",
                "metadata": {"size_bytes": 102400}
            }
        }


# Union type for all media items
MediaItemUnion = Union[
    TextItem,
    ImageItem, 
    AudioItem, 
    VideoItem, 
    Model3DItem,
    DocumentItem,
    BinaryItem
]