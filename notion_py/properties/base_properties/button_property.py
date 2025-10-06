from typing import Literal

from pydantic import Field
from ._base_property import BaseProperty, NotionPropertyType


class ButtonProperty(BaseProperty):
    """Notionのbuttonプロパティ"""

    type: Literal[NotionPropertyType.BUTTON] = Field(
        NotionPropertyType.BUTTON, description="プロパティタイプ"
    )

    # buttonプロパティは通常、値を持たない
    pass

    def get_value(self) -> None:
        """
        button プロパティは値を持たないため常にNoneを返す

        Returns:
            None: buttonプロパティはアクション用で、データ値を持たない

        Note:
            - buttonプロパティはNotionでクリックアクションを実行するためのものです
        """
        return None
