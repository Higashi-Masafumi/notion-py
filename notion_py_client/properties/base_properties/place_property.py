from typing import Any, Literal

from pydantic import Field

from ._base_property import BaseProperty, NotionPropertyType


class PlaceProperty(BaseProperty[Literal[NotionPropertyType.PLACE]]):
    """Notionのplaceプロパティ

    返却形状は仕様追加中のため、値は汎用の辞書として保持します。
    """

    type: Literal[NotionPropertyType.PLACE] = Field(
        NotionPropertyType.PLACE, description="プロパティタイプ"
    )

    place: dict[str, Any] | None = Field(
        default=None, description="place情報（API仕様未確定のため汎用辞書）"
    )

    def get_value(self) -> dict[str, Any] | None:
        """place情報を辞書で返す"""
        return self.place

