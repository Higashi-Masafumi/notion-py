from typing import Literal, Union
from pydantic import Field

from ...models import Group, PartialUser, User
from ._base_property import BaseProperty, NotionPropertyType


class PeopleProperty(BaseProperty[Literal[NotionPropertyType.PEOPLE]]):
    """Notionのpeopleプロパティ"""

    type: Literal[NotionPropertyType.PEOPLE] = Field(
        NotionPropertyType.PEOPLE, description="プロパティタイプ"
    )

    people: list[PartialUser | User | Group] = Field(
        default_factory=list, description="ユーザー/グループ配列"
    )

    def get_display_value(self) -> str | int | float | bool | None:
        """ユーザー/グループ名のリストを取得

        Returns:
            str | None: ユーザー/グループ名をカンマ区切りで連結した文字列。選択がない場合はNone
        """
        if len(self.people) == 0:
            return None
        names: list[str] = []
        for person in self.people:
            name = getattr(person, "name", None)
            if name:
                names.append(name)
        return ", ".join(names) if names else None
