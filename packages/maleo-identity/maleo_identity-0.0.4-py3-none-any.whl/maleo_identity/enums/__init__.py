from __future__ import annotations
from .general import MaleoIdentityGeneralEnums
from .user_profile import MaleoIdentityUserProfileEnums
from .user_system_role import MaleoIdentityUserSystemRoleEnums
from .user_organization import MaleoIdentityUserOrganizationEnums
from .organization import MaleoIdentityOrganizationEnums
from .user import MaleoIdentityUserEnums

class MaleoIdentityEnums:
    General = MaleoIdentityGeneralEnums
    UserProfile = MaleoIdentityUserProfileEnums
    UserSystemRole = MaleoIdentityUserSystemRoleEnums
    UserOrganization = MaleoIdentityUserOrganizationEnums
    Organization = MaleoIdentityOrganizationEnums
    User = MaleoIdentityUserEnums