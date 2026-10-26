from typing import Any, Literal

from pydantic import BaseModel, Field, StrictStr

from ._base_config import BasePropertyConfig


class StatusOptionConfig(BaseModel):
    """statusのオプション定義"""

    id: StrictStr = Field(..., description="ステータスオプションID")
    name: StrictStr = Field(..., description="オプション名")
    color: StrictStr = Field(..., description="表示カラー")
    description: StrictStr | None = Field(None, description="オプション説明")


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
    default_option: StrictStr | None = Field(
        ...,
        description=(
            "ページに明示的なStatus値がないときに表示するオプション名。"
            "未設定ならnull。読み取り専用で、options内のnameを指す。"
        ),
    )


class StatusPropertyConfig(
    BasePropertyConfig[Literal["status"]]
):
    """Notionのstatusプロパティ設定"""

    type: Literal["status"] = Field(
        "status", description="プロパティタイプ"
    )
    status: StatusConfig = Field(
        default_factory=lambda: StatusConfig(default_option=None),
        description="status設定",
    )

    def to_dict(self) -> dict[str, Any]:
        """Notion APIに渡す辞書。読み取り専用のdefault_optionは含めない。"""
        return self.model_dump(
            exclude_none=True,
            exclude={"status": {"default_option": True}},
        )
