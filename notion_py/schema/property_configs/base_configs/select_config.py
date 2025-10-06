from __future__ import annotations

from typing import Literal, Self

from pydantic import BaseModel, Field, StrictStr, model_validator

from ._base_config import BasePropertyConfig
from ....properties.base_properties._base_property import NotionPropertyType


class SelectOptionConfig(BaseModel):
    """select/multi_selectのオプション定義"""

    id: StrictStr | None = Field(None, description="既存オプションID")
    name: StrictStr | None = Field(None, description="オプション名")
    color: StrictStr | None = Field(None, description="表示カラー")
    description: StrictStr | None = Field(None, description="オプション説明")

    @model_validator(mode="after")
    def validate_identifier(self) -> Self:
        if not self.id and not self.name:
            raise ValueError("Select option requires either id or name")
        return self


class SelectOptions(BaseModel):
    options: list[SelectOptionConfig] = Field(
        default_factory=list, description="オプション一覧"
    )


class SelectPropertyConfig(BasePropertyConfig):
    """Notionのselectプロパティ設定"""

    type: Literal[NotionPropertyType.SELECT] = Field(
        NotionPropertyType.SELECT, description="プロパティタイプ"
    )
    select: SelectOptions = Field(
        default_factory=SelectOptions, description="select設定"
    )
