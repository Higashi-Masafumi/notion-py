# notion_async_client.py
from __future__ import annotations
import asyncio
import base64
import json
from collections.abc import Sequence
from enum import Enum, auto
from typing import (
    Any,
    Callable,
    Iterable,
    Literal,
    Mapping,
    TypedDict,
    Union,
    cast,
    NotRequired,
)

import httpx

from .api_types import (
    AppendBlockChildrenParameters,
    CreateCommentParameters,
    CreateDatabaseParameters,
    CreatePageParameters,
    DeleteBlockParameters,
    ListBlockChildrenParameters,
    ListCommentsParameters,
    ListUsersParameters,
    QueryDatabaseParameters,
    RetrieveBlockParameters,
    RetrieveDatabaseParameters,
    RetrievePageParameters,
    RetrieveUserParameters,
    SearchParameters,
    UpdateBlockParameters,
    UpdateDatabaseParameters,
    UpdatePageParameters,
)
from .responses.database import NotionDatabase
from .responses.datasource import DataSource
from .responses.page import NotionPage
from .responses.list_response import (
    QueryDatabaseResponse,
    QueryDataSourceResponse,
    ListUsersResponse,
    SearchResponse,
)


# ========== logging ==========
class LogLevel(Enum):
    DEBUG = auto()
    INFO = auto()
    WARN = auto()
    ERROR = auto()


def _severity(lv: LogLevel) -> int:
    return {
        LogLevel.DEBUG: 10,
        LogLevel.INFO: 20,
        LogLevel.WARN: 30,
        LogLevel.ERROR: 40,
    }[lv]


Logger = Callable[[LogLevel, str, Mapping[str, Any]], None]


def make_console_logger(prefix: str = "notionhq-client") -> Logger:
    def _log(level: LogLevel, message: str, extra: Mapping[str, Any]) -> None:
        print(f"[{prefix}] {level.name:5s} {message} :: {dict(extra)}")

    return _log


# ========== errors ==========
class APIErrorCode(str, Enum):
    Unauthorized = "unauthorized"
    RestrictedResource = "restricted_resource"
    ObjectNotFound = "object_not_found"
    RateLimited = "rate_limited"
    InvalidJSON = "invalid_json"
    InvalidRequestURL = "invalid_request_url"
    InvalidRequest = "invalid_request"
    ValidationError = "validation_error"
    ConflictError = "conflict_error"
    InternalServerError = "internal_server_error"
    ServiceUnavailable = "service_unavailable"


class ClientErrorCode(str, Enum):
    RequestTimeout = "notionhq_client_request_timeout"
    ResponseError = "notionhq_client_response_error"


NotionErrorCode = Union[APIErrorCode, ClientErrorCode]


class NotionClientErrorBase(Exception):
    code: NotionErrorCode


class RequestTimeoutError(NotionClientErrorBase):
    code = ClientErrorCode.RequestTimeout
    name = "RequestTimeoutError"

    def __init__(self, message: str = "Request to Notion API has timed out"):
        super().__init__(message)


class HTTPResponseError(NotionClientErrorBase):
    name = "HTTPResponseError"

    def __init__(
        self,
        *,
        code: NotionErrorCode,
        status: int,
        message: str,
        headers: Mapping[str, str],
        raw_body_text: str,
        additional_data: Mapping[str, Any] | None = None,
        request_id: str | None = None,
    ):
        super().__init__(message)
        self.code = code
        self.status = status
        self.headers = headers
        self.body = raw_body_text
        self.additional_data = additional_data
        self.request_id = request_id


class UnknownHTTPResponseError(HTTPResponseError):
    name = "UnknownHTTPResponseError"

    def __init__(
        self,
        *,
        status: int,
        headers: Mapping[str, str],
        raw_body_text: str,
        message: str | None = None,
    ):
        super().__init__(
            code=ClientErrorCode.ResponseError,
            status=status,
            message=message or f"Request to Notion API failed with status: {status}",
            headers=headers,
            raw_body_text=raw_body_text,
        )


class APIResponseError(HTTPResponseError):
    name = "APIResponseError"


def _parse_api_error_body(body_text: str) -> dict[str, Any] | None:
    try:
        data = json.loads(body_text)
    except Exception:
        return None
    if not isinstance(data, dict):
        return None
    code = data.get("code")
    message = data.get("message")
    if (
        isinstance(code, str)
        and code in set(c.value for c in APIErrorCode)
        and isinstance(message, str)
    ):
        return {
            "code": APIErrorCode(code),
            "message": message,
            "additional_data": data.get("additional_data"),
            "request_id": data.get("request_id"),
        }
    return None


def build_request_error(response: httpx.Response, body_text: str) -> HTTPResponseError:
    parsed = _parse_api_error_body(body_text)
    if parsed:
        return APIResponseError(
            code=parsed["code"],
            status=response.status_code,
            message=parsed["message"],
            headers=dict(response.headers),
            raw_body_text=body_text,
            additional_data=parsed.get("additional_data"),
            request_id=parsed.get("request_id"),
        )
    return UnknownHTTPResponseError(
        status=response.status_code,
        headers=dict(response.headers),
        raw_body_text=body_text,
    )


# ========== utils ==========
def pick(d: Mapping[str, Any], keys: Iterable[str]) -> dict[str, Any]:
    return {k: v for k, v in d.items() if k in keys and v is not None}


def _normalize_query(
    q: Mapping[str, Any] | None,
) -> Sequence[tuple[str, str]] | None:
    """
    クエリパラメータを正規化してhttpx互換の形式に変換。
    多値クエリパラメータ（同じキーで複数の値）を保持するためSequenceを返す。
    """
    if not q:
        return None
    out: list[tuple[str, str]] = []
    for k, v in q.items():
        if v is None:
            continue
        if isinstance(v, (list, tuple)):
            for item in v:
                out.append((k, str(item)))
        else:
            out.append((k, str(v)))
    return out


# ========== client ==========
# Method type (公式SDKと同じ)
Method = Literal["get", "post", "patch", "delete"]

# QueryParams type (公式SDKと同じ)
QueryParams = dict[str, str | int | list[str]]


class FileParam(TypedDict, total=False):
    """ファイルパラメータ (公式SDKのFileParam型)"""

    filename: str
    data: str | bytes  # Pythonでは bytes を使用


class ClientOptions(TypedDict, total=False):
    """
    Notionクライアントのオプション

    Examples:
        ```python
        # 最小構成
        client = NotionAsyncClient(auth="secret_xxx")

        # カスタム設定
        client = NotionAsyncClient(
            auth="secret_xxx",
            options={
                "timeout_ms": 30000,
                "log_level": LogLevel.DEBUG,
                "notion_version": "2025-09-03"
            }
        )
        ```
    """

    timeout_ms: NotRequired[int]
    base_url: NotRequired[str]
    log_level: NotRequired[LogLevel]
    logger: NotRequired[Logger | None]
    notion_version: NotRequired[str]
    user_agent: NotRequired[str]


# AuthParam type (公式SDKと同じ)
AuthParam = Union[
    str,  # Bearer token
    dict[
        str, str
    ],  # {"client_id": "...", "client_secret": "..."}  (OAuthのBasic認可用)
]


class NotionAsyncClient:
    """
    公式JSクライアントの構成を踏襲した async Python クライアント。

    Notion API 2025-09-03に対応:
    - databases: データベース（複数のデータソースを持つコンテナ）の管理
    - dataSources: データソース（実際のデータとスキーマを持つ）の管理・クエリ
    - pages: ページの作成・取得・更新
    - blocks: ブロックの操作
    - users: ユーザー情報の取得
    - comments: コメントの管理
    - fileUploads: ファイルアップロード
    - search: 検索

    重要な概念変更:
    - 旧API: Database = データとスキーマを持つ単一のエンティティ
    - 新API: Database = 複数のDataSourceを持つコンテナ
            DataSource = データとスキーマを持つエンティティ（旧Databaseに相当）

    使い方:
    1. databases.retrieve()でdata_sources一覧を取得
    2. dataSources.query()でデータを取得（旧databases.query()）
    3. dataSources.retrieve()でスキーマを取得（旧databases.retrieve()のproperties部分）
    """

    default_notion_version = "2025-09-03"

    def __init__(self, auth: str, options: ClientOptions | None = None):
        """
        Notionクライアントの初期化

        Args:
            auth: Notion APIの認証トークン（必須）
            options: その他のオプション設定

        Examples:
            ```python
            # シンプルな使い方
            client = NotionAsyncClient(auth="secret_xxx")

            # オプション付き
            client = NotionAsyncClient(
                auth="secret_xxx",
                options={
                    "timeout_ms": 30000,
                    "log_level": LogLevel.DEBUG
                }
            )
            ```
        """
        opts = options or {}
        self._auth = auth
        self._timeout_ms = opts.get("timeout_ms", 60_000)
        base_url = opts.get("base_url", "https://api.notion.com")
        self._prefix_url = f"{base_url.rstrip('/')}/v1/"
        self._notion_version = opts.get("notion_version") or self.default_notion_version
        self._logger = opts.get("logger") or make_console_logger("notionhq-client")
        self._log_level = opts.get("log_level", LogLevel.WARN)
        self._user_agent = opts.get("user_agent", "notionhq-client-python/0.1.0")

        self._client = httpx.AsyncClient(timeout=self._timeout_ms / 1000)

        # ------- public API groups（JSに合わせた名前/階層）-------
        self.blocks = _BlocksAPI(self)
        self.databases = _DatabasesAPI(self)
        self.dataSources = _DataSourcesAPI(self)
        self.pages = _PagesAPI(self)
        self.users = _UsersAPI(self)
        self.comments = _CommentsAPI(self)
        self.fileUploads = _FileUploadsAPI(self)

    # ---------- lifecycle ----------
    async def aclose(self) -> None:
        await self._client.aclose()

    async def __aenter__(self) -> "NotionAsyncClient":
        return self

    async def __aexit__(self, exc_type, exc, tb) -> None:
        await self.aclose()

    # ---------- auth header ----------
    def _auth_as_headers(self, auth: AuthParam | None) -> dict[str, str]:
        headers: dict[str, str] = {}
        auth_value = auth if auth is not None else self._auth
        if isinstance(auth_value, str):
            headers["authorization"] = f"Bearer {auth_value}"
        elif isinstance(auth_value, dict):
            cid = auth_value.get("client_id", "")
            sec = auth_value.get("client_secret", "")
            token = base64.b64encode(f"{cid}:{sec}".encode()).decode()
            headers["authorization"] = f"Basic {token}"
        return headers

    def _log(self, level: LogLevel, message: str, extra: Mapping[str, Any]) -> None:
        if _severity(level) >= _severity(self._log_level):
            self._logger(level, message, extra)

    # ---------- request core ----------
    async def request(
        self,
        *,
        path: str,
        method: Method,
        query: QueryParams | None = None,
        body: dict[str, Any] | None = None,
        form_data_params: dict[str, str | FileParam] | None = None,
        headers: dict[str, str] | None = None,
        auth: AuthParam | None = None,
    ) -> dict[str, Any]:
        url = f"{self._prefix_url}{path}"
        self._log(LogLevel.INFO, "request start", {"method": method, "path": path})

        # headers (優先順: std headers < auth headers < request headers)
        # 右側が優先されるため、標準→認証→呼び出し側の順で展開
        req_headers: dict[str, str] = {
            "Notion-Version": self._notion_version,
            "user-agent": self._user_agent,
            **self._auth_as_headers(auth),
            **(headers or {}),
        }

        json_payload: str | None = None
        files_payload: dict[str, tuple[str | None, Any, str | None]] | None = None

        if form_data_params:
            # multipart/form-data
            # httpx は files に (name, (filename, content, content_type)) を渡す
            files_payload = {}
            for k, v in form_data_params.items():
                if isinstance(v, str):
                    files_payload[k] = (None, v, None)
                else:
                    filename = v.get("filename") if isinstance(v, dict) else None
                    data_value = v.get("data") if isinstance(v, dict) else None
                    if isinstance(data_value, str):
                        data_value = data_value.encode()
                    files_payload[k] = (filename, data_value, None)
        else:
            if body and len(body) > 0:
                json_payload = json.dumps(body)
                req_headers["content-type"] = "application/json"

        # クエリ整形（多値クエリを保持するためリストのまま渡す）
        params = _normalize_query(query)

        # タイムアウト（JSの RequestTimeoutError 相当）
        async def _send() -> httpx.Response:
            return await self._client.request(
                method.upper(),
                url,
                headers=req_headers,
                content=json_payload,
                params=cast(
                    Any, params
                ),  # httpxはSequence[tuple[str, str]]を受け入れる
                files=files_payload,
            )

        try:
            response: httpx.Response = await asyncio.wait_for(
                _send(), timeout=self._timeout_ms / 1000
            )
        except asyncio.TimeoutError:
            self._log(
                LogLevel.WARN,
                "request fail",
                {"code": ClientErrorCode.RequestTimeout, "message": "timeout"},
            )
            raise RequestTimeoutError()

        text = await response.aread()
        text_str = text.decode(errors="replace")

        if not (200 <= response.status_code < 300):
            err = build_request_error(response, text_str)
            self._log(
                LogLevel.WARN,
                "request fail",
                {
                    "code": getattr(err, "code", "unknown"),
                    "message": str(err),
                    **(
                        {"requestId": getattr(err, "request_id")}
                        if getattr(err, "request_id", None)
                        else {}
                    ),
                },
            )
            raise err

        data: dict[str, Any] = json.loads(text_str) if text_str else {}
        self._log(
            LogLevel.INFO,
            "request success",
            {
                "method": method,
                "path": path,
                **(
                    {"requestId": data.get("request_id")}
                    if data.get("request_id")
                    else {}
                ),
            },
        )
        return data

    # ---------- search ----------
    async def search(
        self, params: SearchParameters, *, auth: AuthParam | None = None
    ) -> SearchResponse:
        """
        Search pages and databases

        Args:
            params: 検索パラメータ（クエリ、フィルター、ソート）
            auth: 認証トークン（オプション）

        Examples:
            ```python
            from api_types import SearchParameters

            results = await client.search({
                "query": "プロジェクト",
                "filter": {"property": "object", "value": "page"},
                "page_size": 20
            })
            ```
        """
        response = await self.request(
            path="search", method="post", body=dict(params), auth=auth
        )
        # dict を SearchResponse に変換
        from .responses.page import PartialPage
        from .responses.database import PartialDatabase

        results = []
        for item in response.get("results", []):
            obj_type = item.get("object")
            if obj_type == "page":
                if "properties" in item:
                    results.append(NotionPage(**item))
                else:
                    results.append(PartialPage(**item))
            elif obj_type == "database":
                if "properties" in item:
                    results.append(NotionDatabase(**item))
                else:
                    results.append(PartialDatabase(**item))

        return SearchResponse(
            object="list",
            results=results,
            next_cursor=response.get("next_cursor"),
            has_more=response.get("has_more", False),
            type="page_or_database",
        )

    # ---------- oauth ----------
    async def oauth_token(
        self,
        *,
        grant_type: str,
        client_id: str,
        client_secret: str,
        code: str | None = None,
        redirect_uri: str | None = None,
        external_account: dict[str, str] | None = None,
    ) -> dict[str, Any]:
        """OAuth token endpoint"""
        body = pick(
            {
                "grant_type": grant_type,
                "code": code,
                "redirect_uri": redirect_uri,
                "external_account": external_account,
            },
            ["grant_type", "code", "redirect_uri", "external_account"],
        )
        return await self.request(
            path="oauth/token",
            method="post",
            body=body,
            auth={"client_id": client_id, "client_secret": client_secret},
        )

    async def oauth_introspect(
        self, *, token: str, client_id: str, client_secret: str
    ) -> dict[str, Any]:
        """OAuth introspect endpoint"""
        body = {"token": token}
        return await self.request(
            path="oauth/introspect",
            method="post",
            body=body,
            auth={"client_id": client_id, "client_secret": client_secret},
        )

    async def oauth_revoke(
        self, *, token: str, client_id: str, client_secret: str
    ) -> dict[str, Any]:
        """OAuth revoke endpoint"""
        body = {"token": token}
        return await self.request(
            path="oauth/revoke",
            method="post",
            body=body,
            auth={"client_id": client_id, "client_secret": client_secret},
        )


# ========== Endpoint groups（JSの形に合わせた薄い Facade） ==========
class _BlocksAPI:
    def __init__(self, client: NotionAsyncClient):
        self._c = client
        self.children = _BlockChildrenAPI(client)

    async def retrieve(
        self, *, block_id: str, auth: AuthParam | None = None
    ) -> dict[str, Any]:
        """Retrieve a block

        Returns:
            BlockObjectResponse | PartialBlockObjectResponse: ブロックオブジェクト
        """
        return await self._c.request(path=f"blocks/{block_id}", method="get", auth=auth)

    async def update(self, *, block_id: str, **body) -> dict[str, Any]:
        """Update a block

        Returns:
            BlockObjectResponse | PartialBlockObjectResponse: 更新されたブロックオブジェクト
        """
        return await self._c.request(
            path=f"blocks/{block_id}", method="patch", body=body
        )

    async def delete(
        self, *, block_id: str, auth: AuthParam | None = None
    ) -> dict[str, Any]:
        """Delete a block

        Returns:
            BlockObjectResponse | PartialBlockObjectResponse: 削除されたブロックオブジェクト（archived=True）
        """
        return await self._c.request(
            path=f"blocks/{block_id}", method="delete", auth=auth
        )


class _BlockChildrenAPI:
    def __init__(self, client: NotionAsyncClient):
        self._c = client

    async def append(
        self,
        *,
        block_id: str,
        children: list[dict[str, Any]],
        after: str | None = None,
        auth: AuthParam | None = None,
    ) -> dict[str, Any]:
        """Append block children

        Returns:
            AppendBlockChildrenResponse: 追加された子ブロックを含むレスポンス
        """
        body = {"children": children, **({"after": after} if after else {})}
        return await self._c.request(
            path=f"blocks/{block_id}/children", method="patch", body=body, auth=auth
        )

    async def list(
        self,
        *,
        block_id: str,
        start_cursor: str | None = None,
        page_size: int | None = None,
        auth: AuthParam | None = None,
    ) -> dict[str, Any]:
        """List block children

        Returns:
            ListBlockChildrenResponse: 子ブロックのリスト
        """
        query = pick(
            {"start_cursor": start_cursor, "page_size": page_size},
            ["start_cursor", "page_size"],
        )
        return await self._c.request(
            path=f"blocks/{block_id}/children", method="get", query=query, auth=auth
        )


class _DatabasesAPI:
    """
    Databases API - 2025-09-03対応

    データベースは複数のデータソースを持つコンテナです。
    - databases.retrieve(): データベースのメタ情報とdata_sources一覧を取得
    - databases.create(): 新しいデータベースと初期データソースを作成
    - databases.update(): データベースレベルの属性（title, icon, cover等）を更新

    データのクエリやスキーマ操作はdataSources APIを使用してください。
    """

    def __init__(self, client: NotionAsyncClient):
        self._c = client

    async def retrieve(
        self, params: RetrieveDatabaseParameters, *, auth: AuthParam | None = None
    ) -> NotionDatabase:
        """
        Retrieve a database (API version 2025-09-03)

        データベースのメタ情報とdata_sources一覧を取得します。
        propertiesは含まれません。スキーマ情報が必要な場合は
        dataSources.retrieve(data_source_id)を使用してください。

        Args:
            params: データベース取得パラメータ
            auth: 認証トークン（オプション）

        Returns:
            NotionDatabase: データベースオブジェクト（data_sources配列を含む）

        Examples:
            ```python
            # データベース情報を取得
            db = await client.databases.retrieve(
                {"database_id": "abc123"}
            )

            # データソース一覧を確認
            for ds in db.data_sources:
                print(f"Data Source: {ds['name']} (ID: {ds['id']})")

            # 最初のデータソースのスキーマを取得
            if db.data_sources:
                ds_id = db.data_sources[0]["id"]
                data_source = await client.dataSources.retrieve(
                    data_source_id=ds_id
                )
            ```
        """
        response = await self._c.request(
            path=f"databases/{params['database_id']}", method="get", auth=auth
        )
        return NotionDatabase(**response)

    async def create(
        self, params: CreateDatabaseParameters, *, auth: AuthParam | None = None
    ) -> NotionDatabase:
        """
        Create a database (API version 2025-09-03)

        新しいデータベースと初期データソースを作成します。
        initial_data_sourceにpropertiesを指定してください。

        Returns:
            NotionDatabase: 作成されたデータベースオブジェクト

        Examples:
            ```python
            db = await client.databases.create({
                "parent": {"type": "page_id", "page_id": "parent_page_id"},
                "title": [{"text": {"content": "My Database"}}],
                "initial_data_source": {
                    "properties": {
                        "Name": {"title": {}},
                        "Status": {"select": {"options": [...]}}
                    }
                }
            })
            ```
        """
        response = await self._c.request(
            path="databases", method="post", body=dict(params), auth=auth
        )
        return NotionDatabase(**response)

    async def update(
        self, params: UpdateDatabaseParameters, *, auth: AuthParam | None = None
    ) -> NotionDatabase:
        """
        Update a database (API version 2025-09-03)

        データベースレベルの属性を更新します。
        更新可能: title, icon, cover, is_inline, parent

        データソースのpropertiesを変更する場合は
        dataSources.update()を使用してください。

        Returns:
            NotionDatabase: 更新されたデータベースオブジェクト

        Examples:
            ```python
            # データベースのタイトルを変更
            db = await client.databases.update({
                "database_id": "abc123",
                "title": [{"text": {"content": "New Title"}}]
            })
            ```
        """
        database_id = params["database_id"]
        body = {k: v for k, v in params.items() if k != "database_id"}
        response = await self._c.request(
            path=f"databases/{database_id}",
            method="patch",
            body=body,
            auth=auth,
        )
        return NotionDatabase(**response)


class _DataSourcesAPI:
    """
    Data Sources API - 2025-09-03対応

    データソースは旧APIでの「データベース」の概念に相当します。
    - 実際のデータ（ページ）を持つ
    - スキーマ（properties）を持つ
    - クエリ、作成、更新が可能

    データベースは複数のデータソースを持つコンテナとなりました。
    """

    def __init__(self, client: NotionAsyncClient):
        self._c = client

    async def retrieve(
        self, *, data_source_id: str, auth: AuthParam | None = None
    ) -> DataSource:
        """
        Retrieve a data source (API version 2025-09-03)

        データソースのスキーマ情報（properties）を取得します。
        これは旧APIのdatabases.retrieve()に相当します。

        Args:
            data_source_id: データソースID
            auth: 認証トークン（オプション）

        Returns:
            DataSource: データソースオブジェクト（propertiesを含む）

        Examples:
            ```python
            # データソースのスキーマを取得
            ds = await client.dataSources.retrieve(
                data_source_id="ds_abc123"
            )

            # プロパティを確認
            for name, config in ds.properties.items():
                print(f"{name}: {config.type}")
            ```
        """
        response = await self._c.request(
            path=f"data_sources/{data_source_id}", method="get", auth=auth
        )
        return DataSource(**response)

    async def query(
        self,
        *,
        data_source_id: str,
        filter: dict[str, Any] | None = None,
        sorts: list[dict[str, Any]] | None = None,
        start_cursor: str | None = None,
        page_size: int | None = None,
        auth: AuthParam | None = None,
    ) -> QueryDataSourceResponse:
        """
        Query a data source (API version 2025-09-03)

        データソース内のページ（データ行）を取得します。
        これは旧APIのdatabases.query()に相当します。

        Args:
            data_source_id: データソースID
            filter: フィルター条件
            sorts: ソート条件
            start_cursor: ページネーション用カーソル
            page_size: 取得件数（最大100）
            auth: 認証トークン（オプション）

        Returns:
            QueryDataSourceResponse: クエリ結果（results, has_more, next_cursorを含む）

        Examples:
            ```python
            # データソースからページを取得
            response = await client.dataSources.query(
                data_source_id="ds_abc123",
                page_size=50,
                filter={
                    "property": "Status",
                    "select": {"equals": "Done"}
                }
            )

            for page in response.results:
                if isinstance(page, NotionPage):
                    print(f"Page: {page.id}")

            # ページネーション
            if response.has_more:
                next_response = await client.dataSources.query(
                    data_source_id="ds_abc123",
                    start_cursor=response.next_cursor
                )
            ```
        """
        body = pick(
            {
                "filter": filter,
                "sorts": sorts,
                "start_cursor": start_cursor,
                "page_size": page_size,
            },
            ["filter", "sorts", "start_cursor", "page_size"],
        )
        response = await self._c.request(
            path=f"data_sources/{data_source_id}/query",
            method="post",
            body=body,
            auth=auth,
        )

        # dictの結果をNotionPage/PartialPageに変換
        from .responses.page import PartialPage

        results = []
        for item in response.get("results", []):
            if "properties" in item:
                results.append(NotionPage(**item))
            else:
                results.append(PartialPage(**item))

        return QueryDataSourceResponse(
            object="list",
            results=results,
            next_cursor=response.get("next_cursor"),
            has_more=response.get("has_more", False),
            type="page_or_data_source",
        )

    async def create(
        self,
        *,
        parent: dict[str, Any],
        title: list[dict[str, Any]] | None = None,
        properties: dict[str, Any],
        auth: AuthParam | None = None,
        **kwargs,
    ) -> DataSource:
        """
        Create a data source (API version 2025-09-03)

        既存のデータベースに新しいデータソースを追加します。

        Args:
            parent: 親データベース（{"type": "database_id", "database_id": "..."}）
            title: データソースのタイトル
            properties: スキーマ定義
            auth: 認証トークン（オプション）

        Returns:
            DataSource: 作成されたデータソースオブジェクト

        Examples:
            ```python
            ds = await client.dataSources.create(
                parent={"type": "database_id", "database_id": "db_abc123"},
                title=[{"text": {"content": "New Data Source"}}],
                properties={
                    "Name": {"title": {}},
                    "Status": {"select": {"options": [...]}}
                }
            )
            ```
        """
        body = {
            "parent": parent,
            "properties": properties,
            **pick({"title": title, **kwargs}, ["title"]),
        }
        response = await self._c.request(
            path="data_sources", method="post", body=body, auth=auth
        )
        return DataSource(**response)

    async def update(
        self,
        *,
        data_source_id: str,
        title: list[dict[str, Any]] | None = None,
        properties: dict[str, Any] | None = None,
        auth: AuthParam | None = None,
        **kwargs,
    ) -> DataSource:
        """
        Update a data source (API version 2025-09-03)

        データソースのスキーマ（properties）やタイトルを更新します。

        Args:
            data_source_id: データソースID
            title: 新しいタイトル
            properties: 更新するプロパティ（既存のプロパティを削除するにはnullを指定）
            auth: 認証トークン（オプション）

        Returns:
            DataSource: 更新されたデータソースオブジェクト

        Examples:
            ```python
            # プロパティを追加・削除
            ds = await client.dataSources.update(
                data_source_id="ds_abc123",
                properties={
                    "New Field": {"checkbox": {}},  # 追加
                    "Old Field": None  # 削除
                }
            )
            ```
        """
        body = pick(
            {"title": title, "properties": properties, **kwargs},
            ["title", "properties"],
        )
        response = await self._c.request(
            path=f"data_sources/{data_source_id}", method="patch", body=body, auth=auth
        )
        return DataSource(**response)


class _PagesAPI:
    def __init__(self, client: NotionAsyncClient):
        self._c = client
        self.properties = _PagePropertiesAPI(client)

    async def create(
        self, params: CreatePageParameters, *, auth: AuthParam | None = None
    ) -> NotionPage:
        """Create a page

        Returns:
            NotionPage: 作成されたページオブジェクト
        """
        response = await self._c.request(
            path="pages", method="post", body=dict(params), auth=auth
        )
        return NotionPage(**response)

    async def retrieve(
        self, params: RetrievePageParameters, *, auth: AuthParam | None = None
    ) -> NotionPage:
        """Retrieve a page

        Returns:
            NotionPage: ページオブジェクト
        """
        from typing import cast

        page_id = params["page_id"]
        query_params = {k: v for k, v in params.items() if k != "page_id"}
        response = await self._c.request(
            path=f"pages/{page_id}",
            method="get",
            query=cast(QueryParams, query_params) if query_params else None,
            auth=auth,
        )
        return NotionPage(**response)

    async def update(
        self, params: UpdatePageParameters, *, auth: AuthParam | None = None
    ) -> NotionPage:
        """Update a page

        Returns:
            NotionPage: 更新されたページオブジェクト
        """
        page_id = params["page_id"]
        body = {k: v for k, v in params.items() if k != "page_id"}
        response = await self._c.request(
            path=f"pages/{page_id}", method="patch", body=body, auth=auth
        )
        return NotionPage(**response)


class _PagePropertiesAPI:
    def __init__(self, client: NotionAsyncClient):
        self._c = client

    async def retrieve(
        self,
        *,
        page_id: str,
        property_id: str,
        start_cursor: str | None = None,
        page_size: int | None = None,
        auth: AuthParam | None = None,
    ) -> dict[str, Any]:
        """Retrieve a page property item

        Returns:
            PropertyItemObjectResponse: プロパティアイテムオブジェクト（型に応じてtitle, rich_text, number, date, people等の値を含む）
        """
        query = pick(
            {"start_cursor": start_cursor, "page_size": page_size},
            ["start_cursor", "page_size"],
        )
        return await self._c.request(
            path=f"pages/{page_id}/properties/{property_id}",
            method="get",
            query=query,
            auth=auth,
        )


class _UsersAPI:
    def __init__(self, client: NotionAsyncClient):
        self._c = client

    async def retrieve(
        self, *, user_id: str, auth: AuthParam | None = None
    ) -> dict[str, Any]:
        """Retrieve a user

        Returns:
            UserObjectResponse: ユーザーオブジェクト
        """
        return await self._c.request(path=f"users/{user_id}", method="get", auth=auth)

    async def list(
        self,
        *,
        start_cursor: str | None = None,
        page_size: int | None = None,
        auth: AuthParam | None = None,
    ) -> ListUsersResponse:
        """List all users

        Returns:
            ListUsersResponse: ユーザーのリスト
        """
        query = pick(
            {"start_cursor": start_cursor, "page_size": page_size},
            ["start_cursor", "page_size"],
        )
        response = await self._c.request(
            path="users", method="get", query=query, auth=auth
        )
        from .models.user import PartialUser

        return ListUsersResponse(
            object="list",
            results=[PartialUser(**user) for user in response.get("results", [])],
            next_cursor=response.get("next_cursor"),
            has_more=response.get("has_more", False),
            type="user",
        )

    async def me(self, *, auth: AuthParam | None = None) -> dict[str, Any]:
        """Get details about bot

        Returns:
            UserObjectResponse: ボットユーザーの詳細
        """
        return await self._c.request(path="users/me", method="get", auth=auth)


class _CommentsAPI:
    def __init__(self, client: NotionAsyncClient):
        self._c = client

    async def create(
        self,
        *,
        parent: dict[str, Any],
        rich_text: list[dict[str, Any]],
        discussion_id: str | None = None,
        auth: AuthParam | None = None,
    ) -> dict[str, Any]:
        """Create a comment

        Returns:
            CommentObjectResponse: 作成されたコメントオブジェクト
        """
        body = {
            "parent": parent,
            "rich_text": rich_text,
            **pick({"discussion_id": discussion_id}, ["discussion_id"]),
        }
        return await self._c.request(
            path="comments", method="post", body=body, auth=auth
        )

    async def list(
        self,
        *,
        block_id: str | None = None,
        start_cursor: str | None = None,
        page_size: int | None = None,
        auth: AuthParam | None = None,
    ) -> dict[str, Any]:
        """List comments

        Returns:
            ListCommentsResponse: コメントのリスト（object="list", type="comment", results=CommentObjectResponse[]）
        """
        query = pick(
            {
                "block_id": block_id,
                "start_cursor": start_cursor,
                "page_size": page_size,
            },
            ["block_id", "start_cursor", "page_size"],
        )
        return await self._c.request(
            path="comments", method="get", query=query, auth=auth
        )

    async def retrieve(
        self, *, comment_id: str, auth: AuthParam | None = None
    ) -> dict[str, Any]:
        """Retrieve a comment

        Returns:
            CommentObjectResponse: コメントオブジェクト
        """
        return await self._c.request(
            path=f"comments/{comment_id}", method="get", auth=auth
        )


class _FileUploadsAPI:
    def __init__(self, client: NotionAsyncClient):
        self._c = client

    async def create(
        self,
        *,
        name: str,
        size: int,
        mime_type: str | None = None,
        auth: AuthParam | None = None,
    ) -> dict[str, Any]:
        """Create a file upload

        Returns:
            FileUploadObjectResponse: 作成されたファイルアップロードオブジェクト（upload_urlを含む）
        """
        body = {
            "name": name,
            "size": size,
            **pick({"mime_type": mime_type}, ["mime_type"]),
        }
        return await self._c.request(
            path="file_uploads", method="post", body=body, auth=auth
        )

    async def retrieve(
        self, *, file_upload_id: str, auth: AuthParam | None = None
    ) -> dict[str, Any]:
        """Retrieve a file upload

        Returns:
            FileUploadObjectResponse: ファイルアップロードオブジェクト（status, upload_urlなどを含む）
        """
        return await self._c.request(
            path=f"file_uploads/{file_upload_id}", method="get", auth=auth
        )

    async def list(
        self,
        *,
        start_cursor: str | None = None,
        page_size: int | None = None,
        auth: AuthParam | None = None,
    ) -> dict[str, Any]:
        """List file uploads

        Returns:
            ListFileUploadsResponse: ファイルアップロードのリスト（object="list", type="file_upload", results=FileUploadObjectResponse[]）
        """
        query = pick(
            {"start_cursor": start_cursor, "page_size": page_size},
            ["start_cursor", "page_size"],
        )
        return await self._c.request(
            path="file_uploads", method="get", query=query, auth=auth
        )

    async def send(
        self,
        *,
        file_upload_id: str,
        file: dict[str, Any],
        part_number: str | None = None,
        auth: AuthParam | None = None,
    ) -> dict[str, Any]:
        """
        Send a file upload

        Requires a `file_upload_id`, obtained from the `id` of the Create File
        Upload API response.

        The `file` parameter contains the raw file contents or Blob/File object
        under `file.data`, and an optional `file.filename` string.

        Supply a stringified `part_number` parameter when using file uploads
        in multi-part mode.

        This endpoint sends HTTP multipart/form-data instead of JSON parameters.

        Returns:
            FileUploadPartObjectResponse: アップロードされたパートのレスポンス
        """
        form_data = {
            "file": file,
            **pick({"part_number": part_number}, ["part_number"]),
        }
        return await self._c.request(
            path=f"file_uploads/{file_upload_id}",
            method="post",
            form_data_params=form_data,
            auth=auth,
        )

    async def complete(
        self, *, file_upload_id: str, auth: AuthParam | None = None
    ) -> dict[str, Any]:
        """Complete a file upload

        Returns:
            FileUploadObjectResponse: 完了したファイルアップロードオブジェクト（status="complete"）
        """
        return await self._c.request(
            path=f"file_uploads/{file_upload_id}/complete",
            method="post",
            auth=auth,
        )
