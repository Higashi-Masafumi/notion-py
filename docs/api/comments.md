# Comments API

Create and retrieve comments on pages and blocks.

## Methods

### create

Create a new comment.

```python
async def create(
    *,
    parent: dict[str, Any],
    rich_text: list[dict[str, Any]],
    discussion_id: str | None = None,
    auth: AuthParam | None = None
) -> dict[str, Any]
```

**Example**:

```python
from notion_py_client import NotionAsyncClient

async with NotionAsyncClient(auth="secret_xxx") as client:
    comment = await client.comments.create(
        parent={"page_id": "page_abc123"},
        rich_text=[
            {"type": "text", "text": {"content": "Great work!"}}
        ]
    )

    print(f"Comment ID: {comment['id']}")
```

### list

List comments for a block or page.

```python
async def list(
    *,
    block_id: str | None = None,
    start_cursor: str | None = None,
    page_size: int | None = None,
    auth: AuthParam | None = None
) -> dict[str, Any]
```

**Example**:

```python
async with NotionAsyncClient(auth="secret_xxx") as client:
    response = await client.comments.list(
        block_id="page_abc123",
        page_size=50
    )

    for comment in response["results"]:
        text = comment["rich_text"][0]["plain_text"]
        print(f"Comment: {text}")
```

### retrieve

Retrieve a specific comment.

```python
async def retrieve(
    *,
    comment_id: str,
    auth: AuthParam | None = None
) -> dict[str, Any]
```

**Example**:

```python
async with NotionAsyncClient(auth="secret_xxx") as client:
    comment = await client.comments.retrieve(
        comment_id="comment_abc123"
    )

    print(f"Author: {comment['created_by']['name']}")
```

## Comment Structure

```python
{
    "object": "comment",
    "id": "comment_abc123",
    "parent": {
        "type": "page_id",
        "page_id": "page_abc123"
    },
    "discussion_id": "discussion_abc123",
    "created_time": "2025-01-01T00:00:00.000Z",
    "last_edited_time": "2025-01-01T00:00:00.000Z",
    "created_by": {
        "object": "user",
        "id": "user_abc123"
    },
    "rich_text": [
        {
            "type": "text",
            "text": {"content": "Comment text"},
            "plain_text": "Comment text"
        }
    ]
}
```

## Common Patterns

### Reply to Comment

```python
async with NotionAsyncClient(auth="secret_xxx") as client:
    # Get original comment
    original = await client.comments.retrieve(
        comment_id="comment_abc123"
    )

    # Reply in same discussion
    reply = await client.comments.create(
        parent=original["parent"],
        discussion_id=original["discussion_id"],
        rich_text=[
            {"type": "text", "text": {"content": "Thanks!"}}
        ]
    )
```

### List All Comments

```python
async with NotionAsyncClient(auth="secret_xxx") as client:
    all_comments = []
    cursor = None

    while True:
        response = await client.comments.list(
            block_id="page_abc123",
            start_cursor=cursor,
            page_size=100
        )

        all_comments.extend(response["results"])

        if not response.get("has_more"):
            break

        cursor = response.get("next_cursor")

    print(f"Total comments: {len(all_comments)}")
```
