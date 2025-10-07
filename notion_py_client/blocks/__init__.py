"""
Notionブロックモデル

ブロックタイプごとにファイルを分割して実装
"""

from .base import ApiColor, BlockType, BaseBlockObject, PartialBlock
from .text_blocks import (
    ParagraphBlock,
    Heading1Block,
    Heading2Block,
    Heading3Block,
    BulletedListItemBlock,
    NumberedListItemBlock,
    QuoteBlock,
    ToDoBlock,
    ToggleBlock,
    TemplateBlock,
)
from .special_blocks import (
    SyncedBlockBlock,
    ChildPageBlock,
    ChildDatabaseBlock,
    EquationBlock,
    CodeBlock,
    CalloutBlock,
)
from .layout_blocks import (
    DividerBlock,
    BreadcrumbBlock,
    TableOfContentsBlock,
    ColumnListBlock,
    ColumnBlock,
    LinkToPageBlock,
    TableBlock,
    TableRowBlock,
)
from .media_blocks import (
    EmbedBlock,
    BookmarkBlock,
    ImageBlock,
    VideoBlock,
    PdfBlock,
    FileBlock,
    AudioBlock,
    LinkPreviewBlock,
)
from .unsupported import UnsupportedBlock

# Union type for all block types
BlockObject = (
    ParagraphBlock
    | Heading1Block
    | Heading2Block
    | Heading3Block
    | BulletedListItemBlock
    | NumberedListItemBlock
    | QuoteBlock
    | ToDoBlock
    | ToggleBlock
    | TemplateBlock
    | SyncedBlockBlock
    | ChildPageBlock
    | ChildDatabaseBlock
    | EquationBlock
    | CodeBlock
    | CalloutBlock
    | DividerBlock
    | BreadcrumbBlock
    | TableOfContentsBlock
    | ColumnListBlock
    | ColumnBlock
    | LinkToPageBlock
    | TableBlock
    | TableRowBlock
    | EmbedBlock
    | BookmarkBlock
    | ImageBlock
    | VideoBlock
    | PdfBlock
    | FileBlock
    | AudioBlock
    | LinkPreviewBlock
    | UnsupportedBlock
)

__all__ = [
    # Base
    "ApiColor",
    "BlockType",
    "BaseBlockObject",
    "PartialBlock",
    "BlockObject",
    # Text blocks
    "ParagraphBlock",
    "Heading1Block",
    "Heading2Block",
    "Heading3Block",
    "BulletedListItemBlock",
    "NumberedListItemBlock",
    "QuoteBlock",
    "ToDoBlock",
    "ToggleBlock",
    "TemplateBlock",
    # Special blocks
    "SyncedBlockBlock",
    "ChildPageBlock",
    "ChildDatabaseBlock",
    "EquationBlock",
    "CodeBlock",
    "CalloutBlock",
    # Layout blocks
    "DividerBlock",
    "BreadcrumbBlock",
    "TableOfContentsBlock",
    "ColumnListBlock",
    "ColumnBlock",
    "LinkToPageBlock",
    "TableBlock",
    "TableRowBlock",
    # Media blocks
    "EmbedBlock",
    "BookmarkBlock",
    "ImageBlock",
    "VideoBlock",
    "PdfBlock",
    "FileBlock",
    "AudioBlock",
    "LinkPreviewBlock",
    # Unsupported
    "UnsupportedBlock",
]
