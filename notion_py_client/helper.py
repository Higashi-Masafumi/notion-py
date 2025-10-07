from abc import ABC, abstractmethod
from typing import (
    Any,
    Callable,
    Generic,
    TypeVar,
    overload,
    Never,
)
from pydantic import BaseModel
from .responses.page import NotionPage, PropertyType
from .requests.page_requests import CreatePageParameters, UpdatePageParameters
from .requests.property_requests import PropertyRequest

_TProperty = TypeVar("_TProperty", bound=PropertyType)
_TPropertyRequest = TypeVar("_TPropertyRequest", bound=PropertyRequest | Never)
_TDomainValue = TypeVar("_TDomainValue")


class NotionPropertyDescriptor(
    Generic[_TProperty, _TPropertyRequest, _TDomainValue], ABC
):
    """NotionプロパティとDomainモデル間の双方向変換を提供するディスクリプタ.

    このクラスは以下の機能を提供します:
    - Notionプロパティ値からDomain値への変換（parse）
    - Domain値からNotionプロパティリクエストへの変換（build_request）

    Genericsパラメータ:
        _TProperty: Notionプロパティの型（例: TitleProperty, NumberProperty）
        _TPropertyRequest: プロパティリクエストの型（例: TitlePropertyRequest）
            読み取り専用プロパティの場合はNeverを指定
        _TDomainValue: Domainモデルでの値の型（例: str, int, date）

    Attributes:
        notion_name: Notionでのプロパティ名（例: "名前", "Service"）
        parser: NotionプロパティからDomain値への変換関数
        request_builder: Domain値からPropertyRequestへの変換関数

    Examples:
        >>> # Title プロパティのディスクリプタ
        >>> title_field = NotionPropertyDescriptor(
        ...     notion_name="名前",
        ...     parser=lambda p: p.title[0].plain_text if p.title else "",
        ...     request_builder=lambda v: TitlePropertyRequest(
        ...         title=[{"type": "text", "text": {"content": v}}]
        ...     )
        ... )
        >>>
        >>> # Parse: Notion -> Domain
        >>> domain_value: str = title_field.parse(notion_property)
        >>>
        >>> # Build: Domain -> Notion
        >>> request: TitlePropertyRequest = title_field.build_request("新しい名前")
        >>>
        >>> # 読み取り専用プロパティ（Formula等）
        >>> formula_field: NotionPropertyDescriptor[FormulaProperty, Never, float] = (
        ...     NotionPropertyDescriptor(
        ...         notion_name="契約期間(ヶ月)",
        ...         parser=lambda p: p.formula.number or 0,
        ...         request_builder=None,
        ...     )
        ... )
    """

    def __init__(
        self,
        notion_name: str,
        parser: Callable[[_TProperty], _TDomainValue] | None,
        request_builder: Callable[[_TDomainValue], _TPropertyRequest] | None,
    ):
        """NotionPropertyDescriptorを初期化.

        Args:
            notion_name: Notionでのプロパティ名
            parser: NotionプロパティからDomain値への変換関数。
                Noneの場合は書き込み専用（parseメソッド呼び出し不可）
            request_builder: Domain値からPropertyRequestへの変換関数。
                Noneの場合は読み取り専用（build_requestメソッド呼び出し不可）

        Note:
            Formulaなど読み取り専用プロパティの場合、request_builder=Noneを指定し、
            型パラメータは NotionPropertyDescriptor[FormulaProperty, Never, float] のように
            Neverを使用してください。
        """
        self.notion_name = notion_name
        self.parser = parser
        self.request_builder = request_builder

    def parse(self, property: _TProperty) -> _TDomainValue:
        """NotionプロパティからDomain値へ変換.

        Args:
            property: Notionプロパティオブジェクト

        Returns:
            変換されたDomain値

        Raises:
            ValueError: parserがNone（書き込み専用）の場合
        """
        if self.parser is None:
            raise ValueError(
                f"Property '{self.notion_name}' is write-only and cannot parse values"
            )
        return self.parser(property)

    def build_request(self, value: _TDomainValue) -> _TPropertyRequest:
        """Domain値からNotionプロパティリクエストへ変換.

        Args:
            value: Domain値

        Returns:
            Notionプロパティ更新リクエスト

        Raises:
            ValueError: request_builderがNone（読み取り専用）の場合
        """
        if self.request_builder is None:
            raise ValueError(
                f"Property '{self.notion_name}' is read-only and cannot build requests"
            )
        return self.request_builder(value)


@overload
def Field(
    notion_name: str,
    parser: None = None,
    request_builder: None = None,
) -> NotionPropertyDescriptor[Any, Any, Any]: ...


@overload
def Field(
    notion_name: str,
    parser: Callable[[_TProperty], _TDomainValue],
    request_builder: None = None,
) -> NotionPropertyDescriptor[_TProperty, Any, _TDomainValue]: ...


@overload
def Field(
    notion_name: str,
    parser: None = None,
    request_builder: Callable[[_TDomainValue], _TPropertyRequest] = ...,  # type: ignore
) -> NotionPropertyDescriptor[Any, _TPropertyRequest, _TDomainValue]: ...


@overload
def Field(
    notion_name: str,
    parser: Callable[[_TProperty], _TDomainValue],
    request_builder: Callable[[_TDomainValue], _TPropertyRequest],
) -> NotionPropertyDescriptor[_TProperty, _TPropertyRequest, _TDomainValue]: ...


def Field(
    notion_name: str,
    parser: Callable[[_TProperty], _TDomainValue] | None = None,
    request_builder: Callable[[_TDomainValue], _TPropertyRequest] | None = None,
) -> NotionPropertyDescriptor[Any, Any, Any]:
    """NotionPropertyDescriptorを生成するファクトリ関数.

    型安全なプロパティディスクリプタを生成します。
    parser/request_builderの指定パターンに応じて適切な型推論が行われます。

    Args:
        notion_name: Notionでのプロパティ名
        parser: NotionプロパティからDomain値への変換関数（省略可）
        request_builder: Domain値からPropertyRequestへの変換関数（省略可）

    Returns:
        NotionPropertyDescriptor: 生成されたプロパティディスクリプタ

    Examples:
        >>> # 読み書き可能なフィールド
        >>> service_field = Field(
        ...     notion_name="Service",
        ...     parser=lambda p: p.multi_select[0].name if p.multi_select else "",
        ...     request_builder=lambda v: MultiSelectPropertyRequest(
        ...         multi_select=[{"name": v}]
        ...     )
        ... )
        >>>
        >>> # 読み取り専用フィールド（Formula等）
        >>> duration_field = Field(
        ...     notion_name="契約期間(ヶ月)",
        ...     parser=lambda p: p.formula.number or 0,
        ... )
        >>> # 型は NotionPropertyDescriptor[FormulaProperty, Never, float] として推論される
        >>>
        >>> # 書き込み専用フィールド（稀なケース）
        >>> write_only_field = Field(
        ...     notion_name="SomeProperty",
        ...     request_builder=lambda v: SomePropertyRequest(value=v),
        ... )
    """
    if parser is None:
        parser = lambda _: None  # type: ignore
    if request_builder is None:
        request_builder = lambda _: None  # type: ignore
    return NotionPropertyDescriptor(notion_name, parser, request_builder)  # type: ignore


_TDomainModel = TypeVar("_TDomainModel", bound=BaseModel)


class NotionMapper(Generic[_TDomainModel], ABC):
    """NotionページとDomainモデル間の双方向変換を提供する抽象基底クラス.

    このクラスを継承して具体的なMapperを実装することで、
    NotionページとDomainモデル間の変換ロジックを統一的に管理できます。

    Genericsパラメータ:
        _TDomainModel: 変換対象のDomainモデル型（例: ContractRecord）

    Examples:
        >>> class ContractRecordMapper(NotionMapper[ContractRecord]):
        ...     service_field = Field(
        ...         notion_name="Service",
        ...         parser=lambda p: p.multi_select[0].name if p.multi_select else "",
        ...         request_builder=lambda v: MultiSelectPropertyRequest(
        ...             multi_select=[{"name": v}]
        ...         )
        ...     )
        ...
        ...     def to_domain(self, notion_page: NotionPage) -> ContractRecord:
        ...         props = notion_page.properties
        ...         return ContractRecord(
        ...             id=notion_page.id,
        ...             service=self.service_field.parse(props["Service"]),
        ...             # ...
        ...         )
        ...
        ...     def build_update_properties(
        ...         self, model: ContractRecord
        ...     ) -> UpdatePageParameters:
        ...         return UpdatePageParameters(
        ...             page_id=model.id,
        ...             properties={
        ...                 self.service_field.notion_name: self.service_field.build_request(
        ...                     model.service
        ...                 ),
        ...                 # ...
        ...             }
        ...         )
        ...
        ...     def build_create_properties(
        ...         self, model: ContractRecord
        ...     ) -> CreatePageParameters:
        ...         # 実装省略
        ...         pass
    """

    @abstractmethod
    def to_domain(self, notion_page: NotionPage) -> _TDomainModel:
        """NotionページをDomainモデルに変換.

        Args:
            notion_page: Notionページオブジェクト

        Returns:
            変換されたDomainモデル

        Raises:
            NotImplementedError: サブクラスで実装が必要
        """
        raise NotImplementedError

    @abstractmethod
    def build_update_properties(self, model: _TDomainModel) -> UpdatePageParameters:
        """Domainモデルからページ更新パラメータを構築.

        Args:
            model: Domainモデル（id必須）

        Returns:
            Notionページ更新パラメータ

        Raises:
            NotImplementedError: サブクラスで実装が必要
        """
        raise NotImplementedError

    @abstractmethod
    def build_create_properties(
        self, datasource_id: str, model: _TDomainModel
    ) -> CreatePageParameters:
        """Domainモデルからページ作成パラメータを構築.

        Args:
            model: Domainモデル

        Returns:
            Notionページ作成パラメータ

        Raises:
            NotImplementedError: サブクラスで実装が必要
        """
        raise NotImplementedError
