# Agent Skills API

List plugins and retrieve signed archive URLs for plugin or skill directories.

The client returns the signed URL. It does not download or extract the archive. Requests use the client default `Notion-Version: 2026-03-11`.

## plugins.list

List plugins the connection can read.

```python
async def list(
    *,
    start_cursor: str | None = None,
    page_size: int | None = None,
    auth: AuthParam | None = None
) -> ListPluginsResponse
```

**Example**:

```python
from notion_py_client import NotionAsyncClient

async with NotionAsyncClient(auth="secret_xxx") as client:
    response = await client.plugins.list(page_size=100)

    for plugin in response.results:
        print(plugin.id, plugin.version_id)
```

Each result has `id`, `name`, `description`, and `version_id`. A tagged group of skills and an untagged skill both appear as plugins. Compare `version_id` with the last downloaded value and skip plugins that have not changed.

## plugins.retrieve

Return a signed URL for one plugin directory.

```python
async def retrieve(
    *,
    plugin_id: str,
    auth: AuthParam | None = None
) -> SignedDirectoryResponse
```

**Example**:

```python
archive = await client.plugins.retrieve(plugin_id="plugin_123")
print(archive.url)
```

`url` is a temporary gzipped tar archive.

## skills.retrieve

Return a signed URL for one skill directory. The response shape matches `plugins.retrieve`.

```python
async def retrieve(
    *,
    skill_id: str,
    auth: AuthParam | None = None
) -> SignedDirectoryResponse
```

**Example**:

```python
archive = await client.skills.retrieve(skill_id="skill_123")
print(archive.version_id, archive.url)
```
