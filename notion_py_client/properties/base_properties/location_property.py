from typing import Any, Literal

from pydantic import Field

from ._base_property import BaseProperty, NotionPropertyType


class LocationProperty(BaseProperty[Literal[NotionPropertyType.LOCATION]]):
    """Notionのlocationプロパティ

    現在のNotion APIの更新に伴う新プロパティ。公式の返却形状は将来的に
    変更の可能性があるため、値は汎用の辞書として保持します。
    """

    type: Literal[NotionPropertyType.LOCATION] = Field(
        NotionPropertyType.LOCATION, description="プロパティタイプ"
    )

    location: dict[str, Any] | None = Field(
        default=None, description="ロケーション情報（API仕様未確定のため汎用辞書）"
    )

    def get_value(self) -> dict[str, Any] | None:
        """ロケーション情報を辞書で返す"""
        return self.location

