from typing import Literal

from pydantic import Field

from ._base_config import BasePropertyConfig
from ....models.primitives import EmptyObject


class LocationPropertyConfig(
    BasePropertyConfig[Literal["location"]]
):
    """Notionのlocationプロパティ設定

    TypeScript: LocationPropertyConfigurationRequest
    フィールドは空オブジェクトで構成されます。
    """

    type: Literal["location"] = Field(
        "location", description="プロパティタイプ"
    )
    location: EmptyObject = Field(
        default_factory=EmptyObject, description="location設定"
    )

