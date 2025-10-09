"""
Relation/Peopleフィルター定義

RelationプロパティとPeopleプロパティのフィルター条件。
TypedDict を使用して公式 Notion API 仕様に準拠。

公式TypeScript定義:
type PeoplePropertyFilter =
  | { contains: IdRequest }
  | { does_not_contain: IdRequest }
  | ExistencePropertyFilter

type RelationPropertyFilter =
  | { contains: IdRequest }
  | { does_not_contain: IdRequest }
  | ExistencePropertyFilter
"""

from typing import TypedDict, Union

from .base_filters import ExistencePropertyFilter


# ============================================================================
# People Property Filters
# ============================================================================


class PeopleFilterContains(TypedDict):
    """Peopleが含む

    Examples:
        ```python
        filter: PeopleFilterContains = {"contains": "user-id-123"}
        ```
    """

    contains: str


class PeopleFilterDoesNotContain(TypedDict):
    """Peopleが含まない"""

    does_not_contain: str


# Matches TypeScript: type PeoplePropertyFilter
PeoplePropertyFilter = Union[
    PeopleFilterContains,
    PeopleFilterDoesNotContain,
    ExistencePropertyFilter,
]


# ============================================================================
# Relation Property Filters
# ============================================================================


class RelationFilterContains(TypedDict):
    """Relationが含む

    Examples:
        ```python
        filter: RelationFilterContains = {"contains": "page-id-123"}
        ```
    """

    contains: str


class RelationFilterDoesNotContain(TypedDict):
    """Relationが含まない"""

    does_not_contain: str


# Matches TypeScript: type RelationPropertyFilter
RelationPropertyFilter = Union[
    RelationFilterContains,
    RelationFilterDoesNotContain,
    ExistencePropertyFilter,
]
