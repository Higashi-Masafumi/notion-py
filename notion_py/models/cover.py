"""
Notionカバーモデル

Database、Page、DataSourceなどで使用されるカバー画像の定義
"""

from __future__ import annotations

from enum import Enum

from pydantic import BaseModel, Field

from .file import ExternalFile, InternalFile


class CoverType(str, Enum):
    """カバータイプ"""

    EXTERNAL = "external"
    FILE = "file"


class NotionCover(BaseModel):
    """
    Notionのカバー画像（外部画像または内部ファイル）

    Database、Page、DataSourceで共通使用

    Examples:
        ```python
        # 外部画像カバー
        external_cover = NotionCover(
            type=CoverType.EXTERNAL,
            external=ExternalFile(url="https://example.com/cover.jpg")
        )

        # 内部ファイルカバー
        file_cover = NotionCover(
            type=CoverType.FILE,
            file=InternalFile(url="https://notion.so/...", expiry_time="...")
        )
        ```
    """

    type: CoverType = Field(..., description="カバータイプ")
    external: ExternalFile | None = Field(None, description="外部ファイル")
    file: InternalFile | None = Field(None, description="内部ファイル")
