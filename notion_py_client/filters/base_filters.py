"""
基本的なフィルター定義

存在性チェック等の基本的なフィルター条件。
"""

from typing import Literal, Union

from pydantic import BaseModel, Field


class ExistenceFilter(BaseModel):
    """
    存在性フィルター基底クラス

    プロパティが空かどうかをチェックする。

    Examples:
        ```python
        # 空であることをチェック
        ExistenceFilterEmpty(is_empty=True)

        # 空でないことをチェック
        ExistenceFilterNotEmpty(is_not_empty=True)
        ```
    """

    pass


class ExistenceFilterEmpty(ExistenceFilter):
    """空であることをチェック"""

    is_empty: Literal[True] = Field(True, description="空であることをチェック")


class ExistenceFilterNotEmpty(ExistenceFilter):
    """空でないことをチェック"""

    is_not_empty: Literal[True] = Field(True, description="空でないことをチェック")


ExistencePropertyFilter = Union[ExistenceFilterEmpty, ExistenceFilterNotEmpty]
