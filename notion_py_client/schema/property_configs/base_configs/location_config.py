from typing import Literal

from pydantic import Field

from ._base_config import BasePropertyConfig
from ....models.primitives import EmptyObject
from ....properties.base_properties._base_property import NotionPropertyType


class LocationPropertyConfig(
    BasePropertyConfig[Literal[NotionPropertyType.LOCATION]]
):
    """Notionのlocationプロパティ設定

    TypeScript: LocationPropertyConfigurationRequest
    フィールドは空オブジェクトで構成されます。
    """

    type: Literal[NotionPropertyType.LOCATION] = Field(
        NotionPropertyType.LOCATION, description="プロパティタイプ"
    )
    location: EmptyObject = Field(
        default_factory=EmptyObject, description="location設定"
    )

