from __future__ import annotations
from .organization import MaleoIdentityOrganizationConstants
from .user import MaleoIdentityUserConstants
from .user_profile import MaleoIdentityUserProfileConstants
from .user_system_role import MaleoIdentityUserSystemRoleConstants
from .user_organization import MaleoIdentityUserOrganizationConstants

class MaleoIdentityConstants:
    Organization = MaleoIdentityOrganizationConstants
    User = MaleoIdentityUserConstants
    UserProfile = MaleoIdentityUserProfileConstants
    UserSystemRole = MaleoIdentityUserSystemRoleConstants
    UserOrganization = MaleoIdentityUserOrganizationConstants