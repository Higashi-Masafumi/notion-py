"""Request types for Notion API.

このモジュールは、Notion APIへのリクエストに使用する型定義を提供します。
主にPage作成・更新時のプロパティ値の設定に使用します。
"""

from .common import (
    AnnotationRequest,
    DateRequest,
    GroupObjectRequest,
    IdRequest,
    PartialUserObjectRequest,
    RelationItemRequest,
    SelectPropertyItemRequest,
)
from .page_requests import CreatePageParameters, UpdatePageParameters
from .property_requests import (
    CheckboxPropertyRequest,
    DatePropertyRequest,
    EmailPropertyRequest,
    FilesPropertyRequest,
    MultiSelectPropertyRequest,
    NumberPropertyRequest,
    PeoplePropertyRequest,
    PhoneNumberPropertyRequest,
    PropertyRequest,
    RelationPropertyRequest,
    RichTextPropertyRequest,
    SelectPropertyRequest,
    StatusPropertyRequest,
    TitlePropertyRequest,
    UrlPropertyRequest,
)

__all__ = [
    # Page requests
    "CreatePageParameters",
    "UpdatePageParameters",
    # Property requests
    "PropertyRequest",
    "TitlePropertyRequest",
    "RichTextPropertyRequest",
    "NumberPropertyRequest",
    "UrlPropertyRequest",
    "SelectPropertyRequest",
    "MultiSelectPropertyRequest",
    "PeoplePropertyRequest",
    "EmailPropertyRequest",
    "PhoneNumberPropertyRequest",
    "DatePropertyRequest",
    "CheckboxPropertyRequest",
    "RelationPropertyRequest",
    "FilesPropertyRequest",
    "StatusPropertyRequest",
    # Common types
    "IdRequest",
    "DateRequest",
    "AnnotationRequest",
    "PartialUserObjectRequest",
    "GroupObjectRequest",
    "RelationItemRequest",
    "SelectPropertyItemRequest",
]
