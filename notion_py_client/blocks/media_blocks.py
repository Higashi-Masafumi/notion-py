"""
メディア系ブロックの定義

Embed, Bookmark, Image, Video, PDF, File, Audio, LinkPreview
"""

from __future__ import annotations

from enum import Enum
from typing import Literal

from pydantic import BaseModel, Field, StrictStr

from .base import BaseBlockObject, BlockType
from ..models.rich_text_item import RichTextItem
from ..models.file import InternalFile


class MediaFileType(str, Enum):
    """メディアファイルタイプ"""

    EXTERNAL = "external"
    FILE = "file"


# ============================================
# Content Models
# ============================================


class MediaContentWithUrlAndCaption(BaseModel):
    """URLとキャプションを持つメディアコンテンツ"""

    url: StrictStr = Field(..., description="URL")
    caption: list[RichTextItem] = Field(..., description="キャプション")


class ExternalFileReference(BaseModel):
    """外部ファイル参照"""

    url: StrictStr = Field(..., description="URL")


class ExternalMediaContentWithFileAndCaption(BaseModel):
    """外部ファイルとキャプションを持つメディアコンテンツ"""

    type: Literal[MediaFileType.EXTERNAL] = Field(
        MediaFileType.EXTERNAL, description="ファイルタイプ"
    )
    external: ExternalFileReference = Field(..., description="外部ファイル")
    caption: list[RichTextItem] = Field(..., description="キャプション")


class FileMediaContentWithFileAndCaption(BaseModel):
    """内部ファイルとキャプションを持つメディアコンテンツ"""

    type: Literal[MediaFileType.FILE] = Field(
        MediaFileType.FILE, description="ファイルタイプ"
    )
    file: InternalFile = Field(..., description="内部ファイル")
    caption: list[RichTextItem] = Field(..., description="キャプション")


MediaContentWithFileAndCaption = (
    ExternalMediaContentWithFileAndCaption | FileMediaContentWithFileAndCaption
)


class ExternalMediaContentWithFileNameAndCaption(BaseModel):
    """外部ファイル（ファイル名付き）とキャプションを持つメディアコンテンツ"""

    type: Literal[MediaFileType.EXTERNAL] = Field(
        MediaFileType.EXTERNAL, description="ファイルタイプ"
    )
    external: ExternalFileReference = Field(..., description="外部ファイル")
    caption: list[RichTextItem] = Field(..., description="キャプション")
    name: StrictStr = Field(..., description="ファイル名")


class FileMediaContentWithFileNameAndCaption(BaseModel):
    """内部ファイル（ファイル名付き）とキャプションを持つメディアコンテンツ"""

    type: Literal[MediaFileType.FILE] = Field(
        MediaFileType.FILE, description="ファイルタイプ"
    )
    file: InternalFile = Field(..., description="内部ファイル")
    caption: list[RichTextItem] = Field(..., description="キャプション")
    name: StrictStr = Field(..., description="ファイル名")


MediaContentWithFileNameAndCaption = (
    ExternalMediaContentWithFileNameAndCaption | FileMediaContentWithFileNameAndCaption
)


class MediaContentWithUrl(BaseModel):
    """URLのみを持つメディアコンテンツ"""

    url: StrictStr = Field(..., description="URL")


# ============================================
# Media Blocks
# ============================================


class EmbedBlock(BaseBlockObject):
    """埋め込みブロック"""

    type: Literal[BlockType.EMBED] = Field(
        BlockType.EMBED, description="ブロックタイプ"
    )
    embed: MediaContentWithUrlAndCaption = Field(..., description="埋め込みコンテンツ")


class BookmarkBlock(BaseBlockObject):
    """ブックマークブロック"""

    type: Literal[BlockType.BOOKMARK] = Field(
        BlockType.BOOKMARK, description="ブロックタイプ"
    )
    bookmark: MediaContentWithUrlAndCaption = Field(
        ..., description="ブックマークコンテンツ"
    )


class ImageBlock(BaseBlockObject):
    """画像ブロック"""

    type: Literal[BlockType.IMAGE] = Field(
        BlockType.IMAGE, description="ブロックタイプ"
    )
    image: MediaContentWithFileAndCaption = Field(..., description="画像コンテンツ")


class VideoBlock(BaseBlockObject):
    """動画ブロック"""

    type: Literal[BlockType.VIDEO] = Field(
        BlockType.VIDEO, description="ブロックタイプ"
    )
    video: MediaContentWithFileAndCaption = Field(..., description="動画コンテンツ")


class PdfBlock(BaseBlockObject):
    """PDFブロック"""

    type: Literal[BlockType.PDF] = Field(BlockType.PDF, description="ブロックタイプ")
    pdf: MediaContentWithFileAndCaption = Field(..., description="PDFコンテンツ")


class FileBlock(BaseBlockObject):
    """ファイルブロック"""

    type: Literal[BlockType.FILE] = Field(BlockType.FILE, description="ブロックタイプ")
    file: MediaContentWithFileNameAndCaption = Field(
        ..., description="ファイルコンテンツ"
    )


class AudioBlock(BaseBlockObject):
    """音声ブロック"""

    type: Literal[BlockType.AUDIO] = Field(
        BlockType.AUDIO, description="ブロックタイプ"
    )
    audio: MediaContentWithFileAndCaption = Field(..., description="音声コンテンツ")


class LinkPreviewBlock(BaseBlockObject):
    """リンクプレビューブロック"""

    type: Literal[BlockType.LINK_PREVIEW] = Field(
        BlockType.LINK_PREVIEW, description="ブロックタイプ"
    )
    link_preview: MediaContentWithUrl = Field(
        ..., description="リンクプレビューコンテンツ"
    )
