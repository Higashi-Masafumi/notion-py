from typing import Literal

from pydantic import Field, StrictStr

from ._base_property import BaseProperty


class PhoneNumberProperty(BaseProperty[Literal["phone_number"]]):
    """Notionのphone_numberプロパティ"""

    type: Literal["phone_number"] = Field(
        "phone_number", description="プロパティタイプ"
    )

    phone_number: StrictStr | None = Field(
        None, description="電話番号（未設定の場合はnull）"
    )

    def get_display_value(self) -> str | None:
        """電話番号を取得

        Returns:
            StrictStr | None: 電話番号（未設定の場合はnull）
        """
        return self.phone_number
