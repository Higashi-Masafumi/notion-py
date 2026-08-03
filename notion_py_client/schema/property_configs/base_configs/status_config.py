from typing import Literal

from pydantic import BaseModel, Field, StrictStr

from ._base_config import BasePropertyConfig


class StatusOptionConfig(BaseModel):
    """statusのオプション定義

    スキーマ作成・更新時は ``group`` で ``To-do`` / ``In progress`` / ``Complete``
    のいずれかに割り当てられる。レスポンスでは通常省略され、所属は ``groups`` 側で返る。
    """

    id: StrictStr | None = Field(None, description="ステータスオプションID")
    name: StrictStr = Field(..., description="オプション名")
    color: StrictStr | None = Field(None, description="表示カラー")
    description: StrictStr | None = Field(None, description="オプション説明")
    group: Literal["To-do", "In progress", "Complete"] | None = Field(
        None,
        description="作成・更新時に割り当てるステータスグループ",
    )


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
