"""
サポートされていないブロックの定義
"""

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, Field

from .base import BaseBlockObject, BlockType


class EmptyObject(BaseModel):
    """空のオブジェクト"""

    pass


class UnsupportedBlock(BaseBlockObject):
    """サポートされていないブロック"""

    type: Literal[BlockType.UNSUPPORTED] = Field(
        BlockType.UNSUPPORTED, description="ブロックタイプ"
    )
    unsupported: EmptyObject = Field(
        default_factory=EmptyObject, description="空のコンテンツ"
    )
