from typing import Literal

from pydantic import BaseModel, Field, StrictStr

from ._base_config import BasePropertyConfig
from ....properties.base_properties._base_property import NotionPropertyType


class NumberOptions(BaseModel):
    """numberプロパティの追加設定"""

    format: StrictStr | None = Field(None, description="数値フォーマット")


class NumberPropertyConfig(BasePropertyConfig):
    """Notionのnumberプロパティ設定"""

    type: Literal[NotionPropertyType.NUMBER] = Field(
        NotionPropertyType.NUMBER, description="プロパティタイプ"
    )
    number: NumberOptions = Field(
        default_factory=lambda: NumberOptions(format=None),
        description="数値プロパティ設定",
    )
