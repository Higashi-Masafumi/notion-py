from typing import Literal
from pydantic import Field, StrictFloat, StrictInt

from ._base_property import BaseProperty, NotionPropertyType


class NumberProperty(BaseProperty[Literal[NotionPropertyType.NUMBER]]):
    """Notionのnumberプロパティ"""

    type: Literal[NotionPropertyType.NUMBER] = Field(
        NotionPropertyType.NUMBER, description="プロパティタイプ"
    )

    number: StrictInt | StrictFloat | None = Field(
        None, description="数値（設定されていない場合はnull）"
    )

    def get_display_value(self) -> int | float | None:
        """数値を取得

        Returns:
            StrictInt | StrictFloat | None: 数値（未設定の場合はnull）
        """
        return self.number
