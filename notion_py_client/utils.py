from __future__ import annotations

import re
from typing import (
    Any,
    AsyncIterator,
    Awaitable,
    Callable,
    Mapping,
    Sequence,
    TypeVar,
    Protocol,
    TypeGuard,
    Literal,
)

try:
    from pydantic import BaseModel  # type: ignore
except Exception:  # pragma: no cover - pydantic should exist, but make robust
    BaseModel = object  # type: ignore


# ========= Pagination helpers =========
TItem = TypeVar("TItem")


class _PaginatedResponseLike(Protocol[TItem]):
    """Structural protocol for Notion list responses.

    Works with both dict responses and Pydantic models that expose
    `results`, `next_cursor`, and `has_more` attributes.
    """

    results: Sequence[TItem]
    next_cursor: str | None
    has_more: bool


def _get_attr(obj: Any, key: str, default: Any = None) -> Any:
    """Get attribute or dict item from `obj` with a default."""
    if isinstance(obj, Mapping):
        return obj.get(key, default)
    return getattr(obj, key, default)


async def iterate_paginated_api(
    list_fn: Callable[..., Awaitable[_PaginatedResponseLike[TItem]]],
    first_page_args: Mapping[str, Any] | None = None,
) -> AsyncIterator[TItem]:
    """Iterate over items from any Notion paginated API.

    Mirrors the official TypeScript helper `iteratePaginatedAPI`.

    Example:
        ```python
        async for block in iterate_paginated_api(
            notion.blocks.children.list, {"block_id": parent_block_id}
        ):
            ...
        ```

    Args:
        list_fn: Bound method to a Notion client that returns a paginated list
            object with `results`, `next_cursor`, and `has_more`.
        first_page_args: Arguments to pass on the first and subsequent calls.
            If provided, `start_cursor` will be injected/overwritten as needed.
    """

    args = dict(first_page_args or {})
    next_cursor: str | None = args.get("start_cursor")
    while True:
        # Always pass start_cursor; methods accept None for the first page.
        page_args = {**args, "start_cursor": next_cursor}
        response = await list_fn(**page_args)
        results: Sequence[TItem] = _get_attr(response, "results", [])
        for item in results:
            yield item
        next_cursor = _get_attr(response, "next_cursor")
        if not next_cursor:
            break


async def collect_paginated_api(
    list_fn: Callable[..., Awaitable[_PaginatedResponseLike[TItem]]],
    first_page_args: Mapping[str, Any] | None = None,
) -> list[TItem]:
    """Collect all results from a paginated Notion API into a list.

    Example:
        ```python
        blocks = await collect_paginated_api(
            notion.blocks.children.list, {"block_id": parent_id}
        )
        ```
    """

    out: list[TItem] = []
    async for item in iterate_paginated_api(list_fn, first_page_args):
        out.append(item)
    return out


# ========= Type predicate helpers (TypeScript-like type guards) =========
# Import concrete models for precise TypeGuard targets
from .responses.page import NotionPage, PartialPage
from .responses.datasource import DataSource, PartialDataSource
from .responses.database import NotionDatabase, PartialDatabase
from .blocks.base import BaseBlockObject, PartialBlock
from .models.rich_text_item import RichTextItem
from .models.primitives import Text, Mention, Equation


def _get_object_type(obj: Any) -> str | None:
    return _get_attr(obj, "object")


def is_full_block(
    response: BaseBlockObject | PartialBlock | Mapping[str, Any] | Any,
) -> TypeGuard[BaseBlockObject]:
    """Type guard: block object with full fields (`type` present)."""
    return (
        _get_object_type(response) == "block"
        and _get_attr(response, "type") is not None
    )


def is_full_page(
    response: NotionPage | PartialPage | Mapping[str, Any] | Any,
) -> TypeGuard[NotionPage]:
    """Type guard: page object with full fields (`url` present)."""
    return (
        _get_object_type(response) == "page" and _get_attr(response, "url") is not None
    )


def is_full_data_source(
    response: DataSource | PartialDataSource | Mapping[str, Any] | Any,
) -> TypeGuard[DataSource]:
    """Type guard: data source (full schema object)."""
    return (
        _get_object_type(response) == "data_source"
        and _get_attr(response, "url") is not None
    )


def is_full_database(
    response: NotionDatabase | PartialDatabase | Mapping[str, Any] | Any,
) -> TypeGuard[NotionDatabase]:
    """Type guard: database (full metadata object)."""
    return _get_object_type(response) == "database" and hasattr(response, "title")


def is_full_page_or_data_source(
    response: (
        NotionPage
        | PartialPage
        | DataSource
        | PartialDataSource
        | Mapping[str, Any]
        | Any
    ),
) -> TypeGuard[NotionPage | DataSource]:
    """Type guard: full Page or full DataSource."""
    obj = _get_object_type(response)
    if obj == "data_source":
        return is_full_data_source(response)
    return is_full_page(response)


from .models.user import PartialUser, User  # type: ignore


def is_full_user(
    response: PartialUser | User | Mapping[str, Any] | Any,
) -> TypeGuard[User]:
    """Type guard: full User object (has `type`)."""
    return _get_attr(response, "type") in ("person", "bot")


def is_full_comment(response: Mapping[str, Any] | Any) -> TypeGuard[Mapping[str, Any]]:
    """Best-effort type guard for comment dicts (created_by present)."""
    return isinstance(response, Mapping) and "created_by" in response


class TextRichTextItem(Protocol):
    type: Literal["text"]
    text: Text
    mention: None
    equation: None


class EquationRichTextItem(Protocol):
    type: Literal["equation"]
    equation: Equation
    text: None
    mention: None


class MentionRichTextItem(Protocol):
    type: Literal["mention"]
    mention: Mention
    text: None
    equation: None


def is_text_rich_text_item_response(
    rich_text: RichTextItem | Mapping[str, Any] | Any,
) -> TypeGuard[TextRichTextItem]:
    """Type guard: rich text item is `text` variant (ensures `.text` not None)."""
    return _get_attr(rich_text, "type") == "text"


def is_equation_rich_text_item_response(
    rich_text: RichTextItem | Mapping[str, Any] | Any,
) -> TypeGuard[EquationRichTextItem]:
    """Type guard: rich text item is `equation` variant (ensures `.equation` not None)."""
    return _get_attr(rich_text, "type") == "equation"


def is_mention_rich_text_item_response(
    rich_text: RichTextItem | Mapping[str, Any] | Any,
) -> TypeGuard[MentionRichTextItem]:
    """Type guard: rich text item is `mention` variant (ensures `.mention` not None)."""
    return _get_attr(rich_text, "type") == "mention"


# ========= Notion ID extractors =========

_UUID_HYPHEN_RE = re.compile(
    r"^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$",
    re.IGNORECASE,
)
_UUID_COMPACT_RE = re.compile(r"^[0-9a-f]{32}$", re.IGNORECASE)


def _format_uuid(compact_id: str) -> str:
    clean = compact_id.lower()
    return (
        f"{clean[0:8]}-"
        f"{clean[8:12]}-"
        f"{clean[12:16]}-"
        f"{clean[16:20]}-"
        f"{clean[20:32]}"
    )


def extract_notion_id(url_or_id: str | None) -> str | None:
    """Extract a Notion UUID from a URL or return the input if already a UUID.

    - Accepts hyphenated UUIDs and 32-char hex (no hyphens).
    - Prioritizes IDs found in the URL path over query parameters to avoid
      accidentally extracting view IDs from `v=` queries.

    Returns the UUID in standard hyphenated format or None if not found.
    """
    if not url_or_id or not isinstance(url_or_id, str):
        return None

    s = url_or_id.strip()
    if _UUID_HYPHEN_RE.fullmatch(s):
        return s.lower()
    if _UUID_COMPACT_RE.fullmatch(s):
        return _format_uuid(s)

    # Prefer path segment IDs like `/...-<32hex>`
    m = re.search(r"/[^/?#]*-([0-9a-f]{32})(?:[/?#]|$)", s, flags=re.IGNORECASE)
    if m and m.group(1):
        return _format_uuid(m.group(1))

    # Then query parameters like ?p=<32hex> or ?page_id=<32hex> or ?database_id=<32hex>
    m = re.search(
        r"[?&](?:p|page_id|database_id)=([0-9a-f]{32})", s, flags=re.IGNORECASE
    )
    if m and m.group(1):
        return _format_uuid(m.group(1))

    # Fallback: any 32-hex sequence
    m = re.search(r"([0-9a-f]{32})", s, flags=re.IGNORECASE)
    if m and m.group(1):
        return _format_uuid(m.group(1))

    return None


def extract_database_id(database_url: str | None) -> str | None:
    """Extract a database ID from a Notion database URL or return None."""
    return extract_notion_id(database_url)


def extract_page_id(page_url: str | None) -> str | None:
    """Extract a page ID from a Notion page URL or return None."""
    return extract_notion_id(page_url)


def extract_block_id(url_with_block: str | None) -> str | None:
    """Extract a block ID from a URL fragment like `#block-<id>` or `#<id>`."""
    if not url_with_block or not isinstance(url_with_block, str):
        return None
    m = re.search(r"#(?:block-)?([0-9a-f]{32})", url_with_block, flags=re.IGNORECASE)
    if m and m.group(1):
        return _format_uuid(m.group(1))
    return None
