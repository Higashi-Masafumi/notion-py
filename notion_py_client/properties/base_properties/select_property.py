from typing import Literal
from pydantic import Field

from ...models import SelectOption
from ._base_property import BaseProperty, NotionPropertyType


class SelectProperty(BaseProperty[Literal[NotionPropertyType.SELECT]]):
    """Notionのselectプロパティ"""

    type: Literal[NotionPropertyType.SELECT] = Field(
        NotionPropertyType.SELECT, description="プロパティタイプ"
    )

    select: SelectOption | None = Field(
        None, description="選択されたオプション（設定されていない場合はnull）"
    )

    def get_display_value(self) -> str | None:
        """選択されたオプション名を取得

        Returns:
            str | None: 選択されたオプション名。未設定の場合はNone
        """
        if self.select is None:
            return None
        return self.select.name
