from typing import Literal

from pydantic import Field

from ._base_config import BasePropertyConfig
from ....models.primitives import EmptyObject


class PlacePropertyConfig(BasePropertyConfig[Literal["place"]]):
    """Notionのplaceプロパティ設定

    TypeScript: PlacePropertyConfigurationRequest
    フィールドは空オブジェクトで構成されます。
    """

    type: Literal["place"] = Field(
        "place", description="プロパティタイプ"
    )
    place: EmptyObject = Field(
        default_factory=EmptyObject, description="place設定"
    )

