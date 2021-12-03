from rest_access_policy import AccessPolicy


class GroupAccessPolicy(AccessPolicy):
    statements = [
        {
            "action": ["create", "partial_update", "destroy", "list", "retrieve"],
            "principal": ["group:admin"],
            "effect": "allow"
        }
    ]

class AddToGroupAccessPolicy(AccessPolicy):
    statements = [
        {
            "action": ["add_user_to_group", "patch"],
            "principal": ["group:admin"],
            "effect": "allow"
        }
    ]