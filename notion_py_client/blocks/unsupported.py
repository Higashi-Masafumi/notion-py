"""
サポートされていないブロックの定義
"""

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, Field

from .base import BaseBlockObject


class EmptyObject(BaseModel):
    """空のオブジェクト"""

    pass


class UnsupportedBlock(BaseBlockObject):
    """サポートされていないブロック"""

    type: Literal["unsupported"] = Field("unsupported", description="ブロックタイプ")
    unsupported: EmptyObject = Field(
        default_factory=EmptyObject, description="空のコンテンツ"
    )
