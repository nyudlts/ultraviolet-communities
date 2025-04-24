from flask import g
from flask_login import current_user
from invenio_communities.members.services.service import MemberService
from invenio_communities.members.services.config import MemberServiceConfig


def get_all_community_roles():
    """Return a list of communities the current user is a member of, with roles."""
    if not current_user.is_authenticated:
        return []

    identity = g.identity
    memberships = []

    try:
        # Manually instantiate MemberService (needed for v12)
        service = MemberService(config=MemberServiceConfig())

        # Call the membership list API
        results = service.read_memberships(identity=identity)

        hits = results.get("memberships", [])

        for hit in hits:
            role=hit[1]
            if role in ('curator','manager','owner'):
              memberships.append({
                "community_id": hit[0],
                "role": hit[1]
              })

    except Exception as e:
        print(f"Error fetching membership for community: {e}")
        memberships.append({
            "error": {e}
        })
        return memberships

    return memberships


def inject_context():
    return dict(get_all_community_roles=get_all_community_roles)
