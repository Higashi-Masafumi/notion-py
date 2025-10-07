from typing import Literal
from pydantic import BaseModel, Field, StrictBool, StrictStr

from .base_properties._base_property import NotionPropertyType

from .base_properties import BaseProperty


class RelationItem(BaseModel):
    """Notionのrelation項目"""

    id: StrictStr = Field(..., description="関連項目ID")


class RelationProperty(BaseProperty):
    """Notionのrelationプロパティ"""

    type: Literal[NotionPropertyType.RELATION] = Field(
        NotionPropertyType.RELATION, description="プロパティタイプ"
    )

    relation: list[RelationItem] = Field(
        default_factory=list, description="関連項目配列"
    )
    has_more: StrictBool = Field(False, description="さらに関連項目があるかどうか")

    def get_value(self) -> list[str]:
        """
        relation プロパティから関連したページIDのリストを取得

        Returns:
            list[str]: 関連したページIDのリスト（関連なしの場合は空リスト）

        Note:
            - ページIDは36文字のUUID形式です
            - has_moreがtrueの場合、さらに関連項目が存在します

        Examples:
            - 単一関連: ["12345678-abcd-1234-efgh-123456789012"]
            - 複数関連: ["12345678-...", "87654321-..."]
            - 関連なし: []
        """
        return [item.id for item in self.relation]
