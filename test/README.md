# Tests for notion-py-client

This directory contains the test suite for notion-py-client.

## Directory Structure

```
test/
├── unit/                    # Unit tests (no API calls)
│   ├── test_filters.py      # Filter classes tests
│   ├── test_property_requests.py  # Property request tests
│   └── test_mapper.py       # Domain mapper tests
├── integration/             # Integration tests (real API calls)
│   ├── test_client.py       # Client API integration tests
│   └── test_mapper.py       # Mapper integration tests
└── conftest.py              # Pytest configuration and fixtures
```

## Running Tests

### Unit Tests Only

```bash
# Run all unit tests
pytest test/unit/

# Run specific test file
pytest test/unit/test_filters.py

# Run specific test class
pytest test/unit/test_filters.py::TestTextPropertyFilter

# Run specific test method
pytest test/unit/test_filters.py::TestTextPropertyFilter::test_contains_filter
```

### Integration Tests

Integration tests require Notion API credentials:

```bash
# Set environment variables
export NOTION_API_TOKEN="your_notion_api_token"
export TEST_DATABASE_ID="your_test_database_id"  # Optional, for database tests
export TEST_DATASOURCE_ID="your_test_datasource_id"  # Required for most tests

# Run integration tests
pytest test/integration/

# Run specific integration test file
pytest test/integration/test_client.py

# Run specific test class
pytest test/integration/test_client.py::TestDataSourcesAPI

# Skip integration tests if credentials not set (tests will be skipped automatically)
pytest test/integration/ -v
pytest test/integration/ -v  # Will show skipped tests
```

### All Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=notion_py_client --cov-report=html

# Run with verbose output
pytest -v

# Run with output from print statements
pytest -s
```

## Test Dependencies

Install test dependencies:

```bash
# Using pip
pip install pytest pytest-asyncio pytest-cov

# Using uv
uv add --dev pytest pytest-asyncio pytest-cov
```

## Writing Tests

### Unit Tests

Unit tests should:

- Not make real API calls
- Test individual components in isolation
- Use mocks for external dependencies
- Be fast and deterministic

Example:

```python
def test_filter_creation():
    """Test creating a filter."""
    filter_obj = TextPropertyFilter(
        property="Name",
        rich_text={"contains": "test"}
    )

    result = filter_obj.model_dump(by_alias=True, exclude_none=True)
    assert result["property"] == "Name"
```

### Integration Tests

Integration tests should:

- Use real Notion API credentials
- Be skipped if credentials not available
- Clean up created resources
- Be marked with `@pytest.mark.asyncio` for async tests

Example:

```python
@pytest.mark.asyncio
async def test_query_datasource(notion_client, test_datasource_id):
    """Test querying a datasource."""
    if not test_datasource_id:
        pytest.skip("TEST_DATASOURCE_ID not set")

    response = await notion_client.dataSources.query(
        data_source_id=test_datasource_id
    )

    assert response is not None
```

## Test Coverage

Current test coverage:

### Unit Tests (79 tests)

- ✅ `test_property_requests.py` - 27 tests
  - All 14 property request types
  - Serialization validation
  - None/empty value handling
- ✅ `test_filters.py` - 36 tests
  - PropertyFilter types (Title, RichText, Number, Date, etc.)
  - Timestamp filters (CreatedTime, LastEditedTime)
  - Compound filters (AND, OR, nested)
  - Edge cases
- ✅ `test_mapper.py` - 16 tests
  - Field factory function
  - NotionPropertyDescriptor
  - NotionMapper abstract class
  - Mock NotionPage conversion
  - Edge cases (empty, None values)

### Integration Tests (17+ tests)

- ✅ `test_client.py` - DataSources, Pages, Blocks, Databases, Users, Search APIs
  - Query with filters, sorts, pagination
  - Create, retrieve, update pages
  - Block children operations
  - User listing and bot info
  - Search with filters and sorting
- ✅ `test_mapper.py` - Real API integration with mapper
  - Query and parse with mapper
  - Multiple pages parsing
  - Field parsing validation

## CI/CD

Tests are automatically run on:

- Every pull request
- Every commit to main branch

Only unit tests are run in CI to avoid requiring API credentials.
