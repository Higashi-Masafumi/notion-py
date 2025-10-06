from typing import Literal
from pydantic import Field

from ...models import Group, PartialUser, User
from ._base_property import BaseProperty, NotionPropertyType


class PeopleProperty(BaseProperty):
    """Notionのpeopleプロパティ"""

    type: Literal[NotionPropertyType.PEOPLE] = Field(
        NotionPropertyType.PEOPLE, description="プロパティタイプ"
    )

    people: list[PartialUser | User | Group] = Field(
        default_factory=list, description="ユーザー/グループ配列"
    )

    def get_value(self) -> list[str]:
        """
        people プロパティからユーザー名のリストを取得

        Returns:
            list[str]: ユーザー名のリスト（空の場合は空リスト）

        Examples:
            - 単一ユーザー: ["田中太郎"]
            - 複数ユーザー: ["田中太郎", "佐藤花子"]
            - 未選択: []
        """
        names: list[str] = []
        for person in self.people:
            name = getattr(person, "name", None)
            if name:
                names.append(name)
        return names
