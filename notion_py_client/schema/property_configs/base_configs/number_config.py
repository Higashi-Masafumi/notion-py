from typing import Literal

from pydantic import BaseModel, Field, StrictStr

from ._base_config import BasePropertyConfig


class NumberOptions(BaseModel):
    """numberプロパティの追加設定"""

    format: StrictStr | None = Field(None, description="数値フォーマット")


class NumberPropertyConfig(BasePropertyConfig[Literal["number"]]):
    """Notionのnumberプロパティ設定"""

    type: Literal["number"] = Field(
        "number", description="プロパティタイプ"
    )
    number: NumberOptions = Field(
        default_factory=lambda: NumberOptions(format=None),
        description="数値プロパティ設定",
    )
