from typing import Any, Literal
import json

from pydantic import Field

from ._base_property import BaseProperty


class LocationProperty(BaseProperty[Literal["location"]]):
    """Notionのlocationプロパティ

    現在のNotion APIの更新に伴う新プロパティ。公式の返却形状は将来的に
    変更の可能性があるため、値は汎用の辞書として保持します。
    """

    type: Literal["location"] = Field("location", description="プロパティタイプ")

    location: dict[str, Any] | None = Field(
        default=None, description="ロケーション情報（API仕様未確定のため汎用辞書）"
    )

    def get_display_value(self) -> str | None:
        """ロケーション情報を取得

        Returns:
            str | None: ロケーション情報の文字列表現。未設定の場合はNone
        """
        if self.location is None:
            return None
        try:
            return json.dumps(self.location, ensure_ascii=False, separators=(",", ":"))
        except Exception:
            return str(self.location)
