"""
Notionアイコンモデル

Database、Page、DataSourceなどで使用されるアイコンの定義
"""

from __future__ import annotations

from enum import Enum

from pydantic import BaseModel, Field, StrictStr

from .file import ExternalFile, InternalFile


class IconType(str, Enum):
    """アイコンタイプ"""

    EMOJI = "emoji"
    EXTERNAL = "external"
    FILE = "file"


class NotionIcon(BaseModel):
    """
    Notionのアイコン（絵文字、外部画像、内部ファイル）

    Database、Page、DataSourceで共通使用

    Examples:
        ```python
        # 絵文字アイコン
        emoji_icon = NotionIcon(type=IconType.EMOJI, emoji="📝")

        # 外部画像アイコン
        external_icon = NotionIcon(
            type=IconType.EXTERNAL,
            external=ExternalFile(url="https://example.com/icon.png")
        )

        # 内部ファイルアイコン
        file_icon = NotionIcon(
            type=IconType.FILE,
            file=InternalFile(url="https://notion.so/...", expiry_time="...")
        )
        ```
    """

    type: IconType = Field(..., description="アイコンタイプ")
    emoji: StrictStr | None = Field(None, description="絵文字アイコン")
    external: ExternalFile | None = Field(None, description="外部ファイル")
    file: InternalFile | None = Field(None, description="内部ファイル")
