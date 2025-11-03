from abc import abstractmethod
from typing import Any, Generic, TypeVar, Literal

from pydantic import BaseModel, Field, StrictStr


# Notion プロパティタイプの文字列リテラル型定義
NotionPropertyType = Literal[
    "title",
    "rich_text",
    "date",
    "number",
    "select",
    "multi_select",
    "people",
    "relation",
    "url",
    "checkbox",
    "formula",
    "status",
    "rollup",
    "button",
    "last_edited_time",
    "email",
    "phone_number",
    "files",
    "created_by",
    "created_time",
    "last_edited_by",
    "unique_id",
    "verification",
    "location",
    "last_visited_time",
    "place",
]

TPropertyType = TypeVar("TPropertyType", bound=NotionPropertyType)


class BaseProperty(BaseModel, Generic[TPropertyType]):
    """Notionプロパティのベースクラス"""

    id: StrictStr | None = Field(None, description="プロパティID")
    # 各サブクラスで特定の Literal[...] によって具体化される
    type: TPropertyType = Field(..., description="プロパティタイプ")

    @abstractmethod
    def get_display_value(self) -> str | int | float | bool | None:
        """Notion UI上でのプロパティの表示用の値を取得"""
        pass
