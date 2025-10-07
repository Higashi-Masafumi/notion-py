from typing import Literal
from pydantic import Field, StrictBool

from ._base_property import BaseProperty, NotionPropertyType


class CheckboxProperty(BaseProperty):
    """Notionのcheckboxプロパティ"""

    type: Literal[NotionPropertyType.CHECKBOX] = Field(
        NotionPropertyType.CHECKBOX, description="プロパティタイプ"
    )

    checkbox: StrictBool = Field(False, description="チェックボックスの状態")

    def get_value(self) -> bool:
        """
        checkbox プロパティからチェック状態を取得

        Returns:
            bool: チェック状態（True: チェック済み、False: 未チェック）

        Examples:
            - チェック済み: True
            - 未チェック: False
        """
        return self.checkbox
