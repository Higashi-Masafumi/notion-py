from typing import Literal
from pydantic import BaseModel, Field, StrictBool, StrictStr

from .base_properties import BaseProperty


class RelationItem(BaseModel):
    """Notionのrelation項目"""

    id: StrictStr = Field(..., description="関連項目ID")


class RelationProperty(BaseProperty[Literal["relation"]]):
    """Notionのrelationプロパティ"""

    type: Literal["relation"] = Field("relation", description="プロパティタイプ")

    relation: list[RelationItem] = Field(
        default_factory=list, description="関連項目配列"
    )
    has_more: StrictBool = Field(False, description="さらに関連項目があるかどうか")

    def get_display_value(self) -> str | None:
        """関連項目のIDリストをカンマ区切りで取得

        Returns:
            StrictStr | None: 関連項目のIDをカンマ区切りで連結した文字列。関連項目がない場合はNone
        """
        if len(self.relation) == 0:
            return None
        return ", ".join(item.id for item in self.relation)
