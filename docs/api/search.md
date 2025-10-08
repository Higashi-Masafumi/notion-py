# Search API

Search for pages and databases across the workspace.

## Method

### search

Search for pages and databases.

```python
async def search(
    params: SearchParameters,
    *,
    auth: AuthParam | None = None
) -> SearchResponse
```

**Parameters**:

- `params.query` (optional): Search query string
- `params.filter` (optional): Filter by object type
- `params.sort` (optional): Sort criteria
- `params.start_cursor` (optional): Pagination cursor
- `params.page_size` (optional): Results per page (max 100)

**Returns**: `SearchResponse` with pages and databases

## Examples

### Basic Search

```python
from notion_py_client import NotionAsyncClient

async with NotionAsyncClient(auth="secret_xxx") as client:
    results = await client.search({
        "query": "project",
        "page_size": 20
    })

    for item in results.results:
        if isinstance(item, NotionPage):
            print(f"Page: {item.id}")
        elif isinstance(item, NotionDatabase):
            print(f"Database: {item.id}")
```

### Filter by Object Type

```python
async with NotionAsyncClient(auth="secret_xxx") as client:
    # Search only pages
    pages = await client.search({
        "query": "meeting notes",
        "filter": {
            "property": "object",
            "value": "page"
        }
    })

    # Search only databases
    databases = await client.search({
        "filter": {
            "property": "object",
            "value": "database"
        }
    })
```

### Sort Results

```python
async with NotionAsyncClient(auth="secret_xxx") as client:
    results = await client.search({
        "query": "report",
        "sort": {
            "direction": "descending",
            "timestamp": "last_edited_time"
        }
    })
```

### Pagination

```python
async with NotionAsyncClient(auth="secret_xxx") as client:
    all_results = []
    cursor = None

    while True:
        response = await client.search({
            "query": "task",
            "start_cursor": cursor,
            "page_size": 100
        })

        all_results.extend(response.results)

        if not response.has_more:
            break

        cursor = response.next_cursor

    print(f"Total results: {len(all_results)}")
```

## Search Parameters

### Filter Options

```python
# Pages only
filter = {
    "property": "object",
    "value": "page"
}

# Databases only
filter = {
    "property": "object",
    "value": "database"
}
```

### Sort Options

```python
# By last edited time (descending)
sort = {
    "direction": "descending",
    "timestamp": "last_edited_time"
}

# By last edited time (ascending)
sort = {
    "direction": "ascending",
    "timestamp": "last_edited_time"
}
```

## Common Patterns

### Search and Process Results

```python
async with NotionAsyncClient(auth="secret_xxx") as client:
    results = await client.search({
        "query": "budget",
        "filter": {"property": "object", "value": "page"}
    })

    for page in results.results:
        if isinstance(page, NotionPage):
            # Get full page details
            full_page = await client.pages.retrieve(
                {"page_id": page.id}
            )

            # Process page
            print(f"Found: {full_page.id}")
```

### Find Recently Edited

```python
async with NotionAsyncClient(auth="secret_xxx") as client:
    recent = await client.search({
        "sort": {
            "direction": "descending",
            "timestamp": "last_edited_time"
        },
        "page_size": 10
    })

    for item in recent.results:
        print(f"{item.id} - {item.last_edited_time}")
```

### Search Specific Database

To search within a specific database, use `dataSources.query()` instead:

```python
async with NotionAsyncClient(auth="secret_xxx") as client:
    results = await client.dataSources.query(
        data_source_id="ds_abc123",
        filter={
            "property": "Name",
            "rich_text": {"contains": "project"}
        }
    )
```

## Response Structure

```python
from notion_py_client.responses.list_response import SearchResponse

response: SearchResponse = {
    "object": "list",
    "results": [
        # NotionPage or NotionDatabase objects
    ],
    "next_cursor": "cursor_string",
    "has_more": false,
    "type": "page_or_database"
}
```

## Limitations

- The search API only returns pages and databases the integration has access to
- Maximum 100 results per request (use pagination for more)
- Query string searches page titles and database names
- Full-text search of page content is not supported
- Use `dataSources.query()` for advanced filtering within databases

## Related

- [Data Sources API](datasources.md) - Advanced database queries
- [Pages API](pages.md) - Page operations
- [Databases API](databases.md) - Database operations
