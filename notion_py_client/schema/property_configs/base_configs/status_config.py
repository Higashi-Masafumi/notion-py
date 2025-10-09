from typing import Literal

from pydantic import BaseModel, Field, StrictStr

from ._base_config import BasePropertyConfig
from ....properties.base_properties._base_property import NotionPropertyType


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


class StatusPropertyConfig(
    BasePropertyConfig[Literal[NotionPropertyType.STATUS]]
):
    """Notionのstatusプロパティ設定"""

    type: Literal[NotionPropertyType.STATUS] = Field(
        NotionPropertyType.STATUS, description="プロパティタイプ"
    )
    status: StatusConfig = Field(default_factory=StatusConfig, description="status設定")
