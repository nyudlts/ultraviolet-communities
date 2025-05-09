import pytest
from flask import g

from invenio_communities.context import get_all_community_roles, inject_context


def test_inject_context(app):
    """Test that inject_context returns expected keys."""
    with app.test_request_context():
        context = inject_context()
        assert "get_all_community_roles" in context
        assert callable(context["get_all_community_roles"])


def test_get_all_community_roles_users(app, db, monkeypatch):
    from flask import g

    from invenio_communities import context

    # Mock the current_user with an authenticated one
    class MockUser:
        is_authenticated = True

    monkeypatch.setattr("invenio_communities.context.current_user", MockUser())

    # Mock MemberService to return a curated list
    def mock_read_memberships(self, identity):
        return {"memberships": [("com-1", "curator"), ("com-2", "reader")]}

    monkeypatch.setattr(
        "invenio_communities.context.MemberService.read_memberships",
        mock_read_memberships,
    )

    with app.test_request_context():
        g.identity = object()
        result = context.get_all_community_roles()
        assert result == [{"community_id": "com-1", "role": "curator"}]
