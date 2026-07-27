"""Unit tests for user response models."""

from notion_py_client.models.user import Person, PersonUser


class TestPersonUser:
    """Test person user response parsing."""

    def test_email_verified_parses(self):
        user = PersonUser.model_validate(
            {
                "object": "user",
                "id": "user_123",
                "name": "Ada",
                "avatar_url": None,
                "type": "person",
                "person": {
                    "email": "ada@example.com",
                    "email_verified": True,
                },
            }
        )

        assert isinstance(user.person, Person)
        assert user.person.email == "ada@example.com"
        assert user.person.email_verified is True
