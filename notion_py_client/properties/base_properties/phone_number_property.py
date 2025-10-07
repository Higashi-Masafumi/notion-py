from typing import Literal

from pydantic import Field, StrictStr

from ._base_property import BaseProperty, NotionPropertyType


class PhoneNumberProperty(BaseProperty):
    """Notionのphone_numberプロパティ"""

    type: Literal[NotionPropertyType.PHONE_NUMBER] = Field(
        NotionPropertyType.PHONE_NUMBER, description="プロパティタイプ"
    )

    phone_number: StrictStr | None = Field(
        None, description="電話番号（未設定の場合はnull）"
    )

    def get_value(self) -> str | None:
        """phone_number プロパティから電話番号を取得"""
        return self.phone_number
