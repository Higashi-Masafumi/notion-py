"""
メディア系ブロックの定義

Embed, Bookmark, Image, Video, PDF, File, Audio, LinkPreview
"""

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, Field, StrictStr

from .base import BaseBlockObject
from ..models.rich_text_item import RichTextItem, rich_text_to_markdown
from ..models.file import InternalFile


# MediaFileType as Literal (TypeScript-style)
MediaFileType = Literal["external", "file"]


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

    type: Literal["external"] = Field("external", description="ファイルタイプ")
    external: ExternalFileReference = Field(..., description="外部ファイル")
    caption: list[RichTextItem] = Field(..., description="キャプション")


class FileMediaContentWithFileAndCaption(BaseModel):
    """内部ファイルとキャプションを持つメディアコンテンツ"""

    type: Literal["file"] = Field("file", description="ファイルタイプ")
    file: InternalFile = Field(..., description="内部ファイル")
    caption: list[RichTextItem] = Field(..., description="キャプション")


MediaContentWithFileAndCaption = (
    ExternalMediaContentWithFileAndCaption | FileMediaContentWithFileAndCaption
)


class ExternalMediaContentWithFileNameAndCaption(BaseModel):
    """外部ファイル（ファイル名付き）とキャプションを持つメディアコンテンツ"""

    type: Literal["external"] = Field("external", description="ファイルタイプ")
    external: ExternalFileReference = Field(..., description="外部ファイル")
    caption: list[RichTextItem] = Field(..., description="キャプション")
    name: StrictStr = Field(..., description="ファイル名")


class FileMediaContentWithFileNameAndCaption(BaseModel):
    """内部ファイル（ファイル名付き）とキャプションを持つメディアコンテンツ"""

    type: Literal["file"] = Field("file", description="ファイルタイプ")
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

    type: Literal["embed"] = Field("embed", description="ブロックタイプ")
    embed: MediaContentWithUrlAndCaption = Field(..., description="埋め込みコンテンツ")

    def to_markdown(self) -> str:
        """埋め込みブロックをMarkdown形式に変換"""
        caption = (
            rich_text_to_markdown(self.embed.caption) if self.embed.caption else ""
        )
        if caption:
            return f"[{caption}]({self.embed.url})"
        return f"[Embed]({self.embed.url})"


class BookmarkBlock(BaseBlockObject):
    """ブックマークブロック"""

    type: Literal["bookmark"] = Field("bookmark", description="ブロックタイプ")
    bookmark: MediaContentWithUrlAndCaption = Field(
        ..., description="ブックマークコンテンツ"
    )

    def to_markdown(self) -> str:
        """ブックマークブロックをMarkdown形式に変換"""
        caption = (
            rich_text_to_markdown(self.bookmark.caption)
            if self.bookmark.caption
            else ""
        )
        if caption:
            return f"[{caption}]({self.bookmark.url})"
        return f"[Bookmark]({self.bookmark.url})"


class ImageBlock(BaseBlockObject):
    """画像ブロック"""

    type: Literal["image"] = Field("image", description="ブロックタイプ")
    image: MediaContentWithFileAndCaption = Field(..., description="画像コンテンツ")

    def to_markdown(self) -> str:
        """画像ブロックをMarkdown形式に変換"""
        caption = (
            rich_text_to_markdown(self.image.caption) if self.image.caption else ""
        )
        if self.image.type == "external":
            url = self.image.external.url
        else:
            url = self.image.file.url
        return f"![{caption}]({url})"


class VideoBlock(BaseBlockObject):
    """動画ブロック"""

    type: Literal["video"] = Field("video", description="ブロックタイプ")
    video: MediaContentWithFileAndCaption = Field(..., description="動画コンテンツ")

    def to_markdown(self) -> str:
        """動画ブロックをMarkdown形式に変換"""
        caption = (
            rich_text_to_markdown(self.video.caption) if self.video.caption else ""
        )
        if self.video.type == "external":
            url = self.video.external.url
        else:
            url = self.video.file.url
        if caption:
            return f"[{caption}]({url})"
        return f"[Video]({url})"


class PdfBlock(BaseBlockObject):
    """PDFブロック"""

    type: Literal["pdf"] = Field("pdf", description="ブロックタイプ")
    pdf: MediaContentWithFileAndCaption = Field(..., description="PDFコンテンツ")

    def to_markdown(self) -> str:
        """PDFブロックをMarkdown形式に変換"""
        caption = rich_text_to_markdown(self.pdf.caption) if self.pdf.caption else ""
        if self.pdf.type == "external":
            url = self.pdf.external.url
        else:
            url = self.pdf.file.url
        if caption:
            return f"[{caption}]({url})"
        return f"[PDF]({url})"


class FileBlock(BaseBlockObject):
    """ファイルブロック"""

    type: Literal["file"] = Field("file", description="ブロックタイプ")
    file: MediaContentWithFileNameAndCaption = Field(
        ..., description="ファイルコンテンツ"
    )

    def to_markdown(self) -> str:
        """ファイルブロックをMarkdown形式に変換"""
        caption = (
            rich_text_to_markdown(self.file.caption)
            if self.file.caption
            else self.file.name
        )
        if self.file.type == "external":
            url = self.file.external.url
        else:
            url = self.file.file.url
        return f"[{caption}]({url})"


class AudioBlock(BaseBlockObject):
    """音声ブロック"""

    type: Literal["audio"] = Field("audio", description="ブロックタイプ")
    audio: MediaContentWithFileAndCaption = Field(..., description="音声コンテンツ")

    def to_markdown(self) -> str:
        """音声ブロックをMarkdown形式に変換"""
        caption = (
            rich_text_to_markdown(self.audio.caption) if self.audio.caption else ""
        )
        if self.audio.type == "external":
            url = self.audio.external.url
        else:
            url = self.audio.file.url
        if caption:
            return f"[{caption}]({url})"
        return f"[Audio]({url})"


class LinkPreviewBlock(BaseBlockObject):
    """リンクプレビューブロック"""

    type: Literal["link_preview"] = Field("link_preview", description="ブロックタイプ")
    link_preview: MediaContentWithUrl = Field(
        ..., description="リンクプレビューコンテンツ"
    )

    def to_markdown(self) -> str:
        """リンクプレビューブロックをMarkdown形式に変換"""
        return f"[Link Preview]({self.link_preview.url})"
