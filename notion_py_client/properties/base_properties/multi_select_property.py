from typing import Literal
from pydantic import Field

from ...models import SelectOption
from ._base_property import BaseProperty, NotionPropertyType


class MultiSelectProperty(BaseProperty):
    """Notionのmulti_selectプロパティ"""

    type: Literal[NotionPropertyType.MULTI_SELECT] = Field(
        NotionPropertyType.MULTI_SELECT, description="プロパティタイプ"
    )

    multi_select: list[SelectOption] = Field(
        default_factory=list, description="選択されたオプション配列"
    )

    def get_value(self) -> list[str]:
        """
        multi_select プロパティから選択されたオプション名のリストを取得

        Returns:
            list[str]: 選択されたオプション名のリスト（未選択の場合は空リスト）

        Examples:
            - 単一選択: ["タグA"]
            - 複数選択: ["タグA", "タグB", "タグC"]
            - 未選択: []
        """
        return [option.name for option in self.multi_select]
