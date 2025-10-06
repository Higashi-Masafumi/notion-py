from typing import Literal
from pydantic import Field

from ...models import SelectOption
from ._base_property import BaseProperty, NotionPropertyType


class SelectProperty(BaseProperty):
    """Notionのselectプロパティ"""

    type: Literal[NotionPropertyType.SELECT] = Field(
        NotionPropertyType.SELECT, description="プロパティタイプ"
    )

    select: SelectOption | None = Field(
        None, description="選択されたオプション（設定されていない場合はnull）"
    )

    def get_value(self) -> str | None:
        """
        select プロパティから選択されたオプション名を取得

        Returns:
            str | None: 選択されたオプション名、未選択の場合はNone

        Examples:
            - 選択済み: "進行中"
            - 未選択: None
        """
        return self.select.name if self.select else None
