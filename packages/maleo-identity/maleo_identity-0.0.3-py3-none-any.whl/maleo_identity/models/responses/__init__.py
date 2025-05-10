from __future__ import annotations
from .organization import MaleoIdentityOrganizationResponses
from .user import MaleoIdentityUserResponses
from .user_profile import MaleoIdentityUserProfileResponses
from .user_system_role import MaleoIdentityUserSystemRoleResponses
from .user_organization import MaleoIdentityUserOrganizationResponses

class MaleoIdentityResponses:
    Organization = MaleoIdentityOrganizationResponses
    User = MaleoIdentityUserResponses
    UserProfile = MaleoIdentityUserProfileResponses
    UserSystemRole = MaleoIdentityUserSystemRoleResponses
    UserOrganization = MaleoIdentityUserOrganizationResponses