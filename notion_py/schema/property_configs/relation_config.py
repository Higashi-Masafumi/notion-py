from typing import Literal

from pydantic import BaseModel, Field, StrictStr

from .base_configs import BasePropertyConfig
from ...models.primitives import EmptyObject
from ...properties.base_properties._base_property import NotionPropertyType


class RelationSingleConfig(BaseModel):
    """単方向のrelation設定"""

    type: Literal["single_property"] = Field(
        "single_property", description="Relation設定タイプ"
    )
    data_source_id: StrictStr = Field(..., description="関連先データソースID")
    single_property: EmptyObject = Field(
        default_factory=EmptyObject, description="単方向設定"
    )


class RelationDualDetails(BaseModel):
    """双方向relationの同期設定"""

    synced_property_id: StrictStr | None = Field(None, description="同期先プロパティID")
    synced_property_name: StrictStr | None = Field(
        None, description="同期先プロパティ名"
    )


class RelationDualConfig(BaseModel):
    """双方向relation設定"""

    type: Literal["dual_property"] = Field(
        "dual_property", description="Relation設定タイプ"
    )
    data_source_id: StrictStr = Field(..., description="関連先データソースID")
    dual_property: RelationDualDetails = Field(
        default_factory=lambda: RelationDualDetails(
            synced_property_id=None, synced_property_name=None
        ),
        description="双方向設定",
    )


RelationConfig = RelationSingleConfig | RelationDualConfig


class RelationPropertyConfig(BasePropertyConfig):
    """Notionのrelationプロパティ設定"""

    type: Literal[NotionPropertyType.RELATION] = Field(
        NotionPropertyType.RELATION, description="プロパティタイプ"
    )
    relation: RelationConfig
