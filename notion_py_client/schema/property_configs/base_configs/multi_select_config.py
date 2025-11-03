from typing import Literal

from pydantic import Field

from ._base_config import BasePropertyConfig
from .select_config import SelectOptions


class MultiSelectOptions(SelectOptions):
    """multi_selectオプション定義"""


class MultiSelectPropertyConfig(
    BasePropertyConfig[Literal["multi_select"]]
):
    """Notionのmulti_selectプロパティ設定"""

    type: Literal["multi_select"] = Field(
        "multi_select", description="プロパティタイプ"
    )
    multi_select: MultiSelectOptions = Field(
        default_factory=MultiSelectOptions, description="multi_select設定"
    )
