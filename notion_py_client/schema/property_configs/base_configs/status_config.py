from __future__ import annotations

from typing import Literal, Self

from pydantic import BaseModel, Field, StrictStr, model_validator

from ._base_config import BasePropertyConfig


class StatusOptionConfig(BaseModel):
    """statusのオプション定義"""

    id: StrictStr | None = Field(None, description="ステータスオプションID")
    name: StrictStr | None = Field(None, description="オプション名")
    color: StrictStr | None = Field(None, description="表示カラー")
    description: StrictStr | None = Field(None, description="オプション説明")
    group: Literal["To-do", "In progress", "Complete"] | None = Field(
        None, description="割り当てるステータスグループ"
    )

    @model_validator(mode="after")
    def validate_identifier(self) -> Self:
        if not self.id and not self.name:
            raise ValueError("Status option requires either id or name")
        return self


class StatusGroupConfig(BaseModel):
    """statusのグループ定義"""

    id: StrictStr = Field(..., description="ステータスグループID")
    name: StrictStr = Field(..., description="グループ名")
    color: StrictStr = Field(..., description="表示カラー")
    option_ids: list[StrictStr] = Field(..., description="このグループ内のオプションID")


class StatusConfig(BaseModel):
    """status設定"""

    options: list[StatusOptionConfig] = Field(
        default_factory=list, description="ステータスオプション一覧"
    )
    groups: list[StatusGroupConfig] = Field(
        default_factory=list, description="ステータスグループ一覧"
    )


class StatusPropertyConfig(
    BasePropertyConfig[Literal["status"]]
):
    """Notionのstatusプロパティ設定"""

    type: Literal["status"] = Field(
        "status", description="プロパティタイプ"
    )
    status: StatusConfig = Field(default_factory=StatusConfig, description="status設定")
