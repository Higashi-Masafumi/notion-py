from typing import Any, Literal, Union

from pydantic import BaseModel, Field, StrictFloat, StrictInt, StrictStr

from .base_properties._base_property import (
    NotionPropertyType,
)

from .base_properties import (
    BaseProperty,
    ButtonProperty,
    CheckboxProperty,
    CreatedByProperty,
    CreatedTimeProperty,
    DateProperty,
    EmailProperty,
    FilesProperty,
    FormulaProperty,
    LastEditedByProperty,
    LastEditedTimeProperty,
    MultiSelectProperty,
    NumberProperty,
    PeopleProperty,
    PhoneNumberProperty,
    RichTextProperty,
    SelectProperty,
    StatusProperty,
    TitleProperty,
    UniqueIdProperty,
    UrlProperty,
    VerificationProperty,
)


class Rollup(BaseModel):
    """Notionのrollup項目"""

    type: StrictStr = Field(..., description="rollupのタイプ（numberまたはarray）")
    number: StrictInt | StrictFloat | None = Field(
        None, description="数値（typeがnumberの場合のみ設定）"
    )
    date: DateProperty | None = Field(
        None, description="日付（typeがdateの場合のみ設定）"
    )
    function: StrictStr = Field(..., description="rollup関数（show_original、sum等）")
    array: (
        list[
            Union[
                ButtonProperty,
                CreatedByProperty,
                CreatedTimeProperty,
                DateProperty,
                EmailProperty,
                FilesProperty,
                NumberProperty,
                PeopleProperty,
                PhoneNumberProperty,
                RichTextProperty,
                StatusProperty,
                TitleProperty,
                UrlProperty,
                SelectProperty,
                MultiSelectProperty,
                CheckboxProperty,
                FormulaProperty,
                LastEditedByProperty,
                LastEditedTimeProperty,
                UniqueIdProperty,
                VerificationProperty,
            ]
        ]
        | None
    ) = Field(None, description="配列（typeがarrayの場合のみ設定）")

    def get_value(self) -> Any:
        """
        rollup プロパティからrollupデータを取得

        Returns:
            Any: rollupデータ
        """
        match self.type:
            case "number":
                return self.number
            case "date":
                return self.date
            case "array":
                if self.array and len(self.array) > 0:
                    return self.array[0].get_value()
                else:
                    return None
            case _:
                return None


class RollupProperty(BaseProperty):
    """Notionのrollupプロパティ"""

    type: Literal[NotionPropertyType.ROLLUP] = Field(
        NotionPropertyType.ROLLUP, description="プロパティタイプ"
    )

    rollup: Rollup = Field(..., description="rollupデータ")

    def get_value(self) -> Any:
        """
        rollup プロパティからrollupデータを取得

        Returns:
            Any: rollupデータの値（number、arrayの最初の要素の値、またはNone）
        """
        return self.rollup.get_value()
