# Users API

Retrieve user information.

## Methods

### retrieve

Retrieve a user by ID.

```python
async def retrieve(
    *,
    user_id: str,
    auth: AuthParam | None = None
) -> dict[str, Any]
```

**Example**:

```python
from notion_py_client import NotionAsyncClient

async with NotionAsyncClient(auth="secret_xxx") as client:
    user = await client.users.retrieve(user_id="user_abc123")
    print(f"Name: {user['name']}")
```

### list

List all users in the workspace.

```python
async def list(
    *,
    start_cursor: str | None = None,
    page_size: int | None = None,
    auth: AuthParam | None = None
) -> ListUsersResponse
```

**Example**:

```python
async with NotionAsyncClient(auth="secret_xxx") as client:
    response = await client.users.list(page_size=100)

    for user in response.results:
        print(f"{user.name} ({user.type})")
```

### me

Get details about the current bot user.

```python
async def me(
    *,
    auth: AuthParam | None = None
) -> dict[str, Any]
```

**Example**:

```python
async with NotionAsyncClient(auth="secret_xxx") as client:
    bot = await client.users.me()
    print(f"Bot name: {bot['name']}")
    print(f"Bot ID: {bot['id']}")
```

## User Types

Users can be either people or bots:

```python
# Person
{
    "object": "user",
    "id": "user_abc123",
    "type": "person",
    "person": {
        "email": "user@example.com"
    },
    "name": "John Doe",
    "avatar_url": "https://..."
}

# Bot
{
    "object": "user",
    "id": "bot_abc123",
    "type": "bot",
    "bot": {
        "owner": {
            "type": "workspace",
            "workspace": true
        },
        "workspace_name": "My Workspace"
    },
    "name": "My Integration",
    "avatar_url": "https://..."
}
```

## Common Patterns

### List All Users

```python
async with NotionAsyncClient(auth="secret_xxx") as client:
    all_users = []
    cursor = None

    while True:
        response = await client.users.list(
            start_cursor=cursor,
            page_size=100
        )

        all_users.extend(response.results)

        if not response.has_more:
            break

        cursor = response.next_cursor

    print(f"Total users: {len(all_users)}")
```

### Filter by User Type

```python
async with NotionAsyncClient(auth="secret_xxx") as client:
    response = await client.users.list()

    people = [u for u in response.results if u.type == "person"]
    bots = [u for u in response.results if u.type == "bot"]

    print(f"People: {len(people)}")
    print(f"Bots: {len(bots)}")
```
