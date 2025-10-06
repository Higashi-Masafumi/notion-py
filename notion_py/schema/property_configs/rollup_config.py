from __future__ import annotations

from typing import Literal, Self

from pydantic import BaseModel, Field, StrictStr, model_validator

from .base_configs import BasePropertyConfig
from ...properties.base_properties._base_property import NotionPropertyType


class RollupSettings(BaseModel):
    """rollupプロパティの設定"""

    function: StrictStr = Field(..., description="集計関数")
    relation_property_name: StrictStr | None = Field(
        None, description="リレーションプロパティ名"
    )
    relation_property_id: StrictStr | None = Field(
        None, description="リレーションプロパティID"
    )
    rollup_property_name: StrictStr | None = Field(
        None, description="ロールアップ対象プロパティ名"
    )
    rollup_property_id: StrictStr | None = Field(
        None, description="ロールアップ対象プロパティID"
    )

    @model_validator(mode="after")
    def validate_references(self) -> Self:
        """relation_property_idまたはrelation_property_nameのいずれかが必須であることを検証"""
        if not self.relation_property_id and not self.relation_property_name:
            raise ValueError(
                "RollupSettings requires either relation_property_id or relation_property_name"
            )
        if not self.rollup_property_id and not self.rollup_property_name:
            raise ValueError(
                "RollupSettings requires either rollup_property_id or rollup_property_name"
            )
        return self


class RollupPropertyConfig(BasePropertyConfig):
    """Notionのrollupプロパティ設定"""

    type: Literal[NotionPropertyType.ROLLUP] = Field(
        NotionPropertyType.ROLLUP, description="プロパティタイプ"
    )
    rollup: RollupSettings
