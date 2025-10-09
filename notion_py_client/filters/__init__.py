"""
Notion API フィルター型定義

データベースクエリ時のフィルタ条件を型安全に定義する。
TypedDict を使用して公式 Notion API 仕様に準拠。

主要なエクスポート:
- PropertyFilter: プロパティフィルター統合型
- TimestampFilter: タイムスタンプフィルター
- create_and_filter/create_or_filter: 複合フィルターヘルパー
- 各種具体的なフィルタータイプ

使用例:
    ```python
    from notion_py_client.filters import create_and_filter

    # TypedDict形式で型安全にフィルター作成
    filter = create_and_filter(
        {"property": "Status", "status": {"equals": "Active"}},
        {"property": "Amount", "number": {"greater_than": 10000}},
    )
    ```
"""

# 基本フィルター
from .base_filters import (
    ExistenceFilterEmpty,
    ExistenceFilterNotEmpty,
    ExistencePropertyFilter,
)

# 値フィルター
from .value_filters import (
    CheckboxFilterEquals,
    CheckboxFilterDoesNotEqual,
    CheckboxPropertyFilter,
    MultiSelectFilterContains,
    MultiSelectFilterDoesNotContain,
    MultiSelectPropertyFilter,
    NumberFilterDoesNotEqual,
    NumberFilterEquals,
    NumberFilterGreaterThan,
    NumberFilterGreaterThanOrEqualTo,
    NumberFilterLessThan,
    NumberFilterLessThanOrEqualTo,
    NumberPropertyFilter,
    SelectFilterDoesNotEqual,
    SelectFilterEquals,
    SelectPropertyFilter,
    StatusFilterDoesNotEqual,
    StatusFilterEquals,
    StatusPropertyFilter,
    TextFilterContains,
    TextFilterDoesNotContain,
    TextFilterDoesNotEqual,
    TextFilterEndsWith,
    TextFilterEquals,
    TextFilterStartsWith,
    TextPropertyFilter,
)

# 日付フィルター
from .date_filters import (
    DateFilterAfter,
    DateFilterBefore,
    DateFilterEquals,
    DateFilterNextMonth,
    DateFilterNextWeek,
    DateFilterNextYear,
    DateFilterOnOrAfter,
    DateFilterOnOrBefore,
    DateFilterPastMonth,
    DateFilterPastWeek,
    DateFilterPastYear,
    DateFilterThisWeek,
    DatePropertyFilter,
)

# Relation/Peopleフィルター
from .relation_filters import (
    PeopleFilterContains,
    PeopleFilterDoesNotContain,
    PeoplePropertyFilter,
    RelationFilterContains,
    RelationFilterDoesNotContain,
    RelationPropertyFilter,
)

# 高度なフィルター
from .advanced_filters import (
    FormulaFilterCheckbox,
    FormulaFilterDate,
    FormulaFilterNumber,
    FormulaFilterString,
    FormulaPropertyFilter,
    RollupFilterAny,
    RollupFilterDate,
    RollupFilterEvery,
    RollupFilterNone,
    RollupFilterNumber,
    RollupPropertyFilter,
    RollupSubfilterCheckbox,
    RollupSubfilterDate,
    RollupSubfilterFiles,
    RollupSubfilterMultiSelect,
    RollupSubfilterNumber,
    RollupSubfilterPeople,
    RollupSubfilterPropertyFilter,
    RollupSubfilterRelation,
    RollupSubfilterRichText,
    RollupSubfilterSelect,
    RollupSubfilterStatus,
    VerificationPropertyStatusFilter,
)

# プロパティフィルター
from .property_filters import (
    PropertyFilter,
    PropertyFilterCheckbox,
    PropertyFilterCreatedBy,
    PropertyFilterCreatedTime,
    PropertyFilterDate,
    PropertyFilterEmail,
    PropertyFilterFiles,
    PropertyFilterFormula,
    PropertyFilterLastEditedBy,
    PropertyFilterLastEditedTime,
    PropertyFilterMultiSelect,
    PropertyFilterNumber,
    PropertyFilterPeople,
    PropertyFilterPhoneNumber,
    PropertyFilterRelation,
    PropertyFilterRichText,
    PropertyFilterRollup,
    PropertyFilterSelect,
    PropertyFilterStatus,
    PropertyFilterTitle,
    PropertyFilterUniqueId,
    PropertyFilterUrl,
    PropertyFilterVerification,
)

# タイムスタンプフィルター
from .timestamp_filters import (
    TimestampCreatedTimeFilter,
    TimestampFilter,
    TimestampLastEditedTimeFilter,
)

# 複合フィルター
from .compound_filters import (
    AndFilterDict,
    FilterCondition,
    OrFilterDict,
    create_and_filter,
    create_or_filter,
)

__all__ = [
    # 基本フィルター
    "ExistenceFilterEmpty",
    "ExistenceFilterNotEmpty",
    "ExistencePropertyFilter",
    # テキストフィルター
    "TextFilterEquals",
    "TextFilterDoesNotEqual",
    "TextFilterContains",
    "TextFilterDoesNotContain",
    "TextFilterStartsWith",
    "TextFilterEndsWith",
    "TextPropertyFilter",
    # 数値フィルター
    "NumberFilterEquals",
    "NumberFilterDoesNotEqual",
    "NumberFilterGreaterThan",
    "NumberFilterLessThan",
    "NumberFilterGreaterThanOrEqualTo",
    "NumberFilterLessThanOrEqualTo",
    "NumberPropertyFilter",
    # チェックボックスフィルター
    "CheckboxFilterEquals",
    "CheckboxFilterDoesNotEqual",
    "CheckboxPropertyFilter",
    # セレクトフィルター
    "SelectFilterEquals",
    "SelectFilterDoesNotEqual",
    "SelectPropertyFilter",
    # マルチセレクトフィルター
    "MultiSelectFilterContains",
    "MultiSelectFilterDoesNotContain",
    "MultiSelectPropertyFilter",
    # ステータスフィルター
    "StatusFilterEquals",
    "StatusFilterDoesNotEqual",
    "StatusPropertyFilter",
    # 日付フィルター
    "DateFilterEquals",
    "DateFilterBefore",
    "DateFilterAfter",
    "DateFilterOnOrBefore",
    "DateFilterOnOrAfter",
    "DateFilterThisWeek",
    "DateFilterPastWeek",
    "DateFilterPastMonth",
    "DateFilterPastYear",
    "DateFilterNextWeek",
    "DateFilterNextMonth",
    "DateFilterNextYear",
    "DatePropertyFilter",
    # Peopleフィルター
    "PeopleFilterContains",
    "PeopleFilterDoesNotContain",
    "PeoplePropertyFilter",
    # Relationフィルター
    "RelationFilterContains",
    "RelationFilterDoesNotContain",
    "RelationPropertyFilter",
    # Formulaフィルター
    "FormulaFilterString",
    "FormulaFilterCheckbox",
    "FormulaFilterNumber",
    "FormulaFilterDate",
    "FormulaPropertyFilter",
    # Rollupフィルター
    "RollupFilterAny",
    "RollupFilterNone",
    "RollupFilterEvery",
    "RollupFilterDate",
    "RollupFilterNumber",
    "RollupPropertyFilter",
    "RollupSubfilterRichText",
    "RollupSubfilterNumber",
    "RollupSubfilterCheckbox",
    "RollupSubfilterSelect",
    "RollupSubfilterMultiSelect",
    "RollupSubfilterRelation",
    "RollupSubfilterDate",
    "RollupSubfilterPeople",
    "RollupSubfilterFiles",
    "RollupSubfilterStatus",
    "RollupSubfilterPropertyFilter",
    # Verificationフィルター
    "VerificationPropertyStatusFilter",
    # プロパティフィルター
    "PropertyFilterTitle",
    "PropertyFilterRichText",
    "PropertyFilterNumber",
    "PropertyFilterCheckbox",
    "PropertyFilterSelect",
    "PropertyFilterMultiSelect",
    "PropertyFilterStatus",
    "PropertyFilterDate",
    "PropertyFilterPeople",
    "PropertyFilterFiles",
    "PropertyFilterUrl",
    "PropertyFilterEmail",
    "PropertyFilterPhoneNumber",
    "PropertyFilterRelation",
    "PropertyFilterCreatedBy",
    "PropertyFilterCreatedTime",
    "PropertyFilterLastEditedBy",
    "PropertyFilterLastEditedTime",
    "PropertyFilterFormula",
    "PropertyFilterUniqueId",
    "PropertyFilterRollup",
    "PropertyFilterVerification",
    "PropertyFilter",
    # タイムスタンプフィルター
    "TimestampCreatedTimeFilter",
    "TimestampLastEditedTimeFilter",
    "TimestampFilter",
    # 複合フィルター
    "AndFilterDict",
    "OrFilterDict",
    "FilterCondition",
    "create_and_filter",
    "create_or_filter",
]
