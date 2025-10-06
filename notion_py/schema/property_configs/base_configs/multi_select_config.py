from typing import Literal

from pydantic import Field

from ._base_config import BasePropertyConfig
from .select_config import SelectOptions
from ....properties.base_properties._base_property import NotionPropertyType


class MultiSelectOptions(SelectOptions):
    """multi_selectオプション定義"""


class MultiSelectPropertyConfig(BasePropertyConfig):
    """Notionのmulti_selectプロパティ設定"""

    type: Literal[NotionPropertyType.MULTI_SELECT] = Field(
        NotionPropertyType.MULTI_SELECT, description="プロパティタイプ"
    )
    multi_select: MultiSelectOptions = Field(
        default_factory=MultiSelectOptions, description="multi_select設定"
    )
