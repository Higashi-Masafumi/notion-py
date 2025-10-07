"""
Relation/Peopleフィルター定義

RelationプロパティとPeopleプロパティのフィルター条件。
"""

from typing import Union

from pydantic import BaseModel, Field, StrictStr

from .base_filters import ExistenceFilterEmpty, ExistenceFilterNotEmpty


# ===== Peopleフィルター =====


class PeopleFilterContains(BaseModel):
    """Peopleが含む"""

    contains: StrictStr = Field(..., description="含むユーザーID")


class PeopleFilterDoesNotContain(BaseModel):
    """Peopleが含まない"""

    does_not_contain: StrictStr = Field(..., description="含まないユーザーID")


PeoplePropertyFilter = Union[
    PeopleFilterContains,
    PeopleFilterDoesNotContain,
    ExistenceFilterEmpty,
    ExistenceFilterNotEmpty,
]


# ===== Relationフィルター =====


class RelationFilterContains(BaseModel):
    """Relationが含む"""

    contains: StrictStr = Field(..., description="含むページID")


class RelationFilterDoesNotContain(BaseModel):
    """Relationが含まない"""

    does_not_contain: StrictStr = Field(..., description="含まないページID")


RelationPropertyFilter = Union[
    RelationFilterContains,
    RelationFilterDoesNotContain,
    ExistenceFilterEmpty,
    ExistenceFilterNotEmpty,
]
