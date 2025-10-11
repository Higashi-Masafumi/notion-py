from typing import Literal

from pydantic import Field

from ._base_config import BasePropertyConfig
from ....models.primitives import EmptyObject
from ....properties.base_properties._base_property import NotionPropertyType


class PlacePropertyConfig(BasePropertyConfig[Literal[NotionPropertyType.PLACE]]):
    """Notionのplaceプロパティ設定

    TypeScript: PlacePropertyConfigurationRequest
    フィールドは空オブジェクトで構成されます。
    """

    type: Literal[NotionPropertyType.PLACE] = Field(
        NotionPropertyType.PLACE, description="プロパティタイプ"
    )
    place: EmptyObject = Field(
        default_factory=EmptyObject, description="place設定"
    )

