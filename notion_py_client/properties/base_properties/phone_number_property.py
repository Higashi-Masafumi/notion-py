from typing import Literal

from pydantic import Field, StrictStr

from ._base_property import BaseProperty, NotionPropertyType


class PhoneNumberProperty(BaseProperty[Literal[NotionPropertyType.PHONE_NUMBER]]):
    """Notionのphone_numberプロパティ"""

    type: Literal[NotionPropertyType.PHONE_NUMBER] = Field(
        NotionPropertyType.PHONE_NUMBER, description="プロパティタイプ"
    )

    phone_number: StrictStr | None = Field(
        None, description="電話番号（未設定の場合はnull）"
    )

    def get_display_value(self) -> StrictStr | int | float | bool | None:
        """電話番号を取得

        Returns:
            StrictStr | None: 電話番号（未設定の場合はnull）
        """
        return self.phone_number
