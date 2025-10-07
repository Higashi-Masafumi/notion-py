from typing import Any

from pydantic import BaseModel, ConfigDict, Field, StrictStr

from ....properties.base_properties._base_property import NotionPropertyType


class BasePropertyConfig(BaseModel):
    """Notionのプロパティ設定のベースクラス"""

    model_config = ConfigDict(extra="forbid", use_enum_values=True)

    type: NotionPropertyType = Field(..., description="プロパティタイプ")
    description: StrictStr | None = Field(None, description="プロパティの説明")

    def to_dict(self) -> dict[str, Any]:
        """Notion APIに渡す辞書形式の設定"""
        return self.model_dump(exclude_none=True)

    def to_json(self) -> str:
        """JSON文字列にシリアライズ"""
        return self.model_dump_json(exclude_none=True)
