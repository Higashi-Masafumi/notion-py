from typing import Literal
from pydantic import Field, StrictFloat, StrictInt

from ._base_property import BaseProperty, NotionPropertyType


class NumberProperty(BaseProperty):
    """Notionのnumberプロパティ"""

    type: Literal[NotionPropertyType.NUMBER] = Field(
        NotionPropertyType.NUMBER, description="プロパティタイプ"
    )

    number: StrictInt | StrictFloat | None = Field(
        None, description="数値（設定されていない場合はnull）"
    )

    def get_value(self) -> int | float | None:
        """
        number プロパティから数値を取得

        Returns:
            int | float | None: 数値、未設定の場合はNone

        Note:
            - Notionで整数として入力されたint、小数として入力されたfloatで返されます

        Examples:
            - 整数: 100
            - 小数: 99.5
            - 未設定: None
        """
        return self.number
