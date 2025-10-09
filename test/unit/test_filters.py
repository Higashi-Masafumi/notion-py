"""Unit tests for filter TypedDicts."""

import pytest
from notion_py_client.filters.property_filters import (
    PropertyFilterTitle,
    PropertyFilterRichText,
    PropertyFilterNumber,
    PropertyFilterCheckbox,
    PropertyFilterSelect,
    PropertyFilterMultiSelect,
    PropertyFilterStatus,
    PropertyFilterDate,
    PropertyFilterPeople,
    PropertyFilterFiles,
    PropertyFilterRelation,
    PropertyFilterFormula,
)
from notion_py_client.filters.timestamp_filters import (
    TimestampCreatedTimeFilter,
    TimestampLastEditedTimeFilter,
)
from notion_py_client.filters.compound_filters import (
    create_and_filter,
    create_or_filter,
    AndFilterDict,
    OrFilterDict,
)


class TestPropertyFilterTitle:
    """Test PropertyFilterTitle TypedDict."""

    def test_contains_filter(self):
        """Test title contains filter."""
        filter_dict: PropertyFilterTitle = {
            "property": "Name",
            "title": {"contains": "test"},
        }

        assert filter_dict["property"] == "Name"
        assert filter_dict["title"]["contains"] == "test"  # type: ignore  # type: ignore

    def test_equals_filter(self):
        """Test title equals filter."""
        filter_dict: PropertyFilterTitle = {
            "property": "Task",
            "title": {"equals": "Done"},
        }

        assert filter_dict["property"] == "Task"
        assert filter_dict["title"]["equals"] == "Done"  # type: ignore  # type: ignore

    def test_is_empty_filter(self):
        """Test title is_empty filter."""
        filter_dict: PropertyFilterTitle = {
            "property": "Description",
            "title": {"is_empty": True},
        }

        assert filter_dict["property"] == "Description"
        assert filter_dict["title"]["is_empty"] is True  # type: ignore  # type: ignore


class TestPropertyFilterRichText:
    """Test PropertyFilterRichText TypedDict."""

    def test_contains_filter(self):
        """Test rich_text contains filter."""
        filter_dict: PropertyFilterRichText = {
            "property": "Notes",
            "rich_text": {"contains": "important"},
        }

        assert filter_dict["property"] == "Notes"
        assert filter_dict["rich_text"]["contains"] == "important"  # type: ignore

    def test_is_not_empty_filter(self):
        """Test rich_text is_not_empty filter."""
        filter_dict: PropertyFilterRichText = {
            "property": "Description",
            "rich_text": {"is_not_empty": True},
        }

        assert filter_dict["rich_text"]["is_not_empty"] is True  # type: ignore


class TestPropertyFilterNumber:
    """Test PropertyFilterNumber TypedDict."""

    def test_equals_filter(self):
        """Test number equals filter."""
        filter_dict: PropertyFilterNumber = {
            "property": "Score",
            "number": {"equals": 100},
        }

        assert filter_dict["property"] == "Score"
        assert filter_dict["number"]["equals"] == 100  # type: ignore

    def test_greater_than_filter(self):
        """Test number greater_than filter."""
        filter_dict: PropertyFilterNumber = {
            "property": "Price",
            "number": {"greater_than": 1000},
        }

        assert filter_dict["number"]["greater_than"] == 1000  # type: ignore

    def test_less_than_or_equal_filter(self):
        """Test number less_than_or_equal_to filter."""
        filter_dict: PropertyFilterNumber = {
            "property": "Quantity",
            "number": {"less_than_or_equal_to": 50},
        }

        assert filter_dict["number"]["less_than_or_equal_to"] == 50  # type: ignore


class TestPropertyFilterCheckbox:
    """Test PropertyFilterCheckbox TypedDict."""

    def test_equals_true_filter(self):
        """Test checkbox equals true filter."""
        filter_dict: PropertyFilterCheckbox = {
            "property": "Completed",
            "checkbox": {"equals": True},
        }

        assert filter_dict["checkbox"]["equals"] is True  # type: ignore

    def test_equals_false_filter(self):
        """Test checkbox equals false filter."""
        filter_dict: PropertyFilterCheckbox = {
            "property": "Archived",
            "checkbox": {"equals": False},
        }

        assert filter_dict["checkbox"]["equals"] is False  # type: ignore


class TestPropertyFilterSelect:
    """Test PropertyFilterSelect TypedDict."""

    def test_equals_filter(self):
        """Test select equals filter."""
        filter_dict: PropertyFilterSelect = {
            "property": "Priority",
            "select": {"equals": "High"},
        }

        assert filter_dict["select"]["equals"] == "High"  # type: ignore

    def test_is_empty_filter(self):
        """Test select is_empty filter."""
        filter_dict: PropertyFilterSelect = {
            "property": "Category",
            "select": {"is_empty": True},
        }

        assert filter_dict["select"]["is_empty"] is True  # type: ignore


class TestPropertyFilterMultiSelect:
    """Test PropertyFilterMultiSelect TypedDict."""

    def test_contains_filter(self):
        """Test multi_select contains filter."""
        filter_dict: PropertyFilterMultiSelect = {
            "property": "Tags",
            "multi_select": {"contains": "urgent"},
        }

        assert filter_dict["multi_select"]["contains"] == "urgent"  # type: ignore

    def test_does_not_contain_filter(self):
        """Test multi_select does_not_contain filter."""
        filter_dict: PropertyFilterMultiSelect = {
            "property": "Labels",
            "multi_select": {"does_not_contain": "archived"},
        }

        assert filter_dict["multi_select"]["does_not_contain"] == "archived"  # type: ignore


class TestPropertyFilterStatus:
    """Test PropertyFilterStatus TypedDict."""

    def test_equals_filter(self):
        """Test status equals filter."""
        filter_dict: PropertyFilterStatus = {
            "property": "Status",
            "status": {"equals": "In Progress"},
        }

        assert filter_dict["property"] == "Status"
        assert filter_dict["status"]["equals"] == "In Progress"  # type: ignore

    def test_does_not_equal_filter(self):
        """Test status does_not_equal filter."""
        filter_dict: PropertyFilterStatus = {
            "property": "State",
            "status": {"does_not_equal": "Cancelled"},
        }

        assert filter_dict["status"]["does_not_equal"] == "Cancelled"  # type: ignore


class TestPropertyFilterDate:
    """Test PropertyFilterDate TypedDict."""

    def test_equals_filter(self):
        """Test date equals filter."""
        filter_dict: PropertyFilterDate = {
            "property": "Due Date",
            "date": {"equals": "2025-10-09"},
        }

        assert filter_dict["date"]["equals"] == "2025-10-09"  # type: ignore

    def test_before_filter(self):
        """Test date before filter."""
        filter_dict: PropertyFilterDate = {
            "property": "Created",
            "date": {"before": "2025-01-01"},
        }

        assert filter_dict["date"]["before"] == "2025-01-01"  # type: ignore

    def test_is_empty_filter(self):
        """Test date is_empty filter."""
        filter_dict: PropertyFilterDate = {
            "property": "Deadline",
            "date": {"is_empty": True},
        }

        assert filter_dict["date"]["is_empty"] is True  # type: ignore


class TestPropertyFilterPeople:
    """Test PropertyFilterPeople TypedDict."""

    def test_contains_filter(self):
        """Test people contains filter."""
        filter_dict: PropertyFilterPeople = {
            "property": "Assignee",
            "people": {"contains": "user-123"},
        }

        assert filter_dict["people"]["contains"] == "user-123"  # type: ignore

    def test_is_empty_filter(self):
        """Test people is_empty filter."""
        filter_dict: PropertyFilterPeople = {
            "property": "Reviewers",
            "people": {"is_empty": True},
        }

        assert filter_dict["people"]["is_empty"] is True  # type: ignore


class TestPropertyFilterFiles:
    """Test PropertyFilterFiles TypedDict."""

    def test_is_empty_filter(self):
        """Test files is_empty filter."""
        filter_dict: PropertyFilterFiles = {
            "property": "Attachments",
            "files": {"is_empty": True},
        }

        assert filter_dict["files"]["is_empty"] is True  # type: ignore

    def test_is_not_empty_filter(self):
        """Test files is_not_empty filter."""
        filter_dict: PropertyFilterFiles = {
            "property": "Documents",
            "files": {"is_not_empty": True},
        }

        assert filter_dict["files"]["is_not_empty"] is True  # type: ignore


class TestPropertyFilterRelation:
    """Test PropertyFilterRelation TypedDict."""

    def test_contains_filter(self):
        """Test relation contains filter."""
        filter_dict: PropertyFilterRelation = {
            "property": "Projects",
            "relation": {"contains": "page-123"},
        }

        assert filter_dict["relation"]["contains"] == "page-123"  # type: ignore

    def test_is_empty_filter(self):
        """Test relation is_empty filter."""
        filter_dict: PropertyFilterRelation = {
            "property": "Dependencies",
            "relation": {"is_empty": True},
        }

        assert filter_dict["relation"]["is_empty"] is True  # type: ignore


class TestPropertyFilterFormula:
    """Test PropertyFilterFormula TypedDict."""

    def test_text_formula_filter(self):
        """Test formula filter with text."""
        filter_dict: PropertyFilterFormula = {
            "property": "Computed",
            "formula": {"text": {"contains": "result"}},  # type: ignore
        }

        assert filter_dict["formula"]["text"]["contains"] == "result"  # type: ignore

    def test_number_formula_filter(self):
        """Test formula filter with number."""
        filter_dict: PropertyFilterFormula = {
            "property": "Total",
            "formula": {"number": {"greater_than": 100}},
        }

        assert filter_dict["formula"]["number"]["greater_than"] == 100  # type: ignore

    def test_checkbox_formula_filter(self):
        """Test formula filter with checkbox."""
        filter_dict: PropertyFilterFormula = {
            "property": "IsValid",
            "formula": {"checkbox": {"equals": True}},
        }

        assert filter_dict["formula"]["checkbox"]["equals"] is True  # type: ignore


class TestTimestampFilters:
    """Test Timestamp filter TypedDicts."""

    def test_created_time_filter(self):
        """Test created_time filter."""
        filter_dict: TimestampCreatedTimeFilter = {
            "timestamp": "created_time",
            "created_time": {"after": "2025-01-01T00:00:00.000Z"},
        }

        assert filter_dict["timestamp"] == "created_time"
        assert filter_dict["created_time"]["after"] == "2025-01-01T00:00:00.000Z"  # type: ignore

    def test_last_edited_time_filter(self):
        """Test last_edited_time filter."""
        filter_dict: TimestampLastEditedTimeFilter = {
            "timestamp": "last_edited_time",
            "last_edited_time": {"before": "2025-12-31T23:59:59.999Z"},
        }

        assert filter_dict["timestamp"] == "last_edited_time"
        assert filter_dict["last_edited_time"]["before"] == "2025-12-31T23:59:59.999Z"  # type: ignore


class TestCompoundFilterHelpers:
    """Test compound filter helper functions."""

    def test_create_and_filter(self):
        """Test create_and_filter helper."""
        filter1: PropertyFilterTitle = {
            "property": "Name",
            "title": {"contains": "test"},
        }
        filter2: PropertyFilterStatus = {
            "property": "Status",
            "status": {"equals": "Done"},
        }

        and_filter = create_and_filter(filter1, filter2)

        assert "and" in and_filter
        assert len(and_filter["and"]) == 2

    def test_create_or_filter(self):
        """Test create_or_filter helper."""
        filter1: PropertyFilterTitle = {
            "property": "Priority",
            "title": {"equals": "High"},
        }
        filter2: PropertyFilterTitle = {
            "property": "Priority",
            "title": {"equals": "Urgent"},
        }

        or_filter = create_or_filter(filter1, filter2)

        assert "or" in or_filter
        assert len(or_filter["or"]) == 2

    def test_nested_compound_filters(self):
        """Test nested AND/OR filters."""
        # Create inner OR filter
        filter1: PropertyFilterStatus = {
            "property": "Status",
            "status": {"equals": "Todo"},
        }
        filter2: PropertyFilterStatus = {
            "property": "Status",
            "status": {"equals": "In Progress"},
        }
        or_filter = create_or_filter(filter1, filter2)

        # Create outer AND filter
        filter3: PropertyFilterPeople = {
            "property": "Assignee",
            "people": {"contains": "user-123"},
        }
        and_filter = create_and_filter(or_filter, filter3)

        assert "and" in and_filter
        assert len(and_filter["and"]) == 2
        assert "or" in and_filter["and"][0]

    def test_and_filter_with_timestamp(self):
        """Test AND filter with timestamp filter."""
        property_filter: PropertyFilterTitle = {
            "property": "Name",
            "title": {"contains": "urgent"},
        }
        timestamp_filter: TimestampCreatedTimeFilter = {
            "timestamp": "created_time",
            "created_time": {"after": "2025-01-01T00:00:00.000Z"},
        }

        and_filter = create_and_filter(property_filter, timestamp_filter)

        assert "and" in and_filter
        assert len(and_filter["and"]) == 2


class TestFilterEdgeCases:
    """Test edge cases and complex filter scenarios."""

    def test_multiple_conditions_and(self):
        """Test AND filter with multiple conditions."""
        filters: list[
            PropertyFilterStatus | PropertyFilterTitle | PropertyFilterPeople
        ] = [
            {"property": "Status", "status": {"equals": "Done"}},
            {"property": "Priority", "title": {"equals": "High"}},
            {"property": "Assignee", "people": {"is_not_empty": True}},
        ]

        and_filter = create_and_filter(*filters)  # type: ignore

        assert len(and_filter["and"]) == 3  # type: ignore

    def test_empty_filter_values(self):
        """Test filters with empty/null checks."""
        empty_filters = [
            {"property": "Notes", "rich_text": {"is_empty": True}},
            {"property": "Files", "files": {"is_empty": True}},
            {"property": "Relations", "relation": {"is_empty": True}},
        ]

        for filter_dict in empty_filters:
            # All should be valid TypedDicts
            assert "property" in filter_dict
