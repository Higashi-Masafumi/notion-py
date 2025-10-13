from typing import Any, Literal
import json

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

    def get_display_value(self) -> str | None:
        """place情報を取得

        Returns:
            str | None: place情報の文字列表現。未設定の場合はNone
        """
        if self.place is None:
            return None
        try:
            return json.dumps(self.place, ensure_ascii=False, separators=(",", ":"))
        except Exception:
            return str(self.place)
