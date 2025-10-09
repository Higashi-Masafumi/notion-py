from typing import Any, Generic, TypeVar

from pydantic import BaseModel, ConfigDict, Field, StrictStr

from ....properties.base_properties._base_property import NotionPropertyType

_TPropertyType = TypeVar("_TPropertyType", bound=NotionPropertyType)


class BasePropertyConfig(BaseModel, Generic[_TPropertyType]):
    """Notionのプロパティ設定のベースクラス"""

    id: StrictStr = Field(..., description="プロパティID")
    name: StrictStr = Field(..., description="プロパティ名")
    type: _TPropertyType
    description: StrictStr | None = Field(None, description="プロパティの説明")

    def to_dict(self) -> dict[str, Any]:
        """Notion APIに渡す辞書形式の設定"""
        return self.model_dump(exclude_none=True)

    def to_json(self) -> str:
        """JSON文字列にシリアライズ"""
        return self.model_dump_json(exclude_none=True)
