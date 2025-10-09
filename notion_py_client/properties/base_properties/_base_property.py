from abc import abstractmethod
from enum import Enum
from typing import Any, Generic, TypeVar

from pydantic import BaseModel, Field, StrictStr


class NotionPropertyType(str, Enum):
    """Notionプロパティタイプの列挙型"""

    TITLE = "title"
    RICH_TEXT = "rich_text"
    DATE = "date"
    NUMBER = "number"
    SELECT = "select"
    MULTI_SELECT = "multi_select"
    PEOPLE = "people"
    RELATION = "relation"
    URL = "url"
    CHECKBOX = "checkbox"
    FORMULA = "formula"
    STATUS = "status"
    ROLLUP = "rollup"
    BUTTON = "button"
    LAST_EDITED_TIME = "last_edited_time"
    EMAIL = "email"
    PHONE_NUMBER = "phone_number"
    FILES = "files"
    CREATED_BY = "created_by"
    CREATED_TIME = "created_time"
    LAST_EDITED_BY = "last_edited_by"
    UNIQUE_ID = "unique_id"
    VERIFICATION = "verification"


TPropertyType = TypeVar("TPropertyType", bound="NotionPropertyType")


class BaseProperty(BaseModel, Generic[TPropertyType]):
    """Notionプロパティのベースクラス"""

    id: StrictStr | None = Field(None, description="プロパティID")
    # 各サブクラスで特定の Literal[...] によって具体化される
    type: TPropertyType = Field(..., description="プロパティタイプ")

    @abstractmethod
    def get_value(self) -> Any:
        """プロパティの値を取得"""
        pass
