from __future__ import annotations
from .organization import MaleoIdentityOrganizationGeneralSchemas
from .user import MaleoIdentityUserGeneralSchemas
from .user_profile import MaleoIdentityUserProfileGeneralSchemas
from .user_system_role import MaleoIdentityUserSystemRoleGeneralSchemas
from .user_organization import MaleoIdentityUserOrganizationGeneralSchemas

class MaleoIdentityGeneralSchemas:
    Organization = MaleoIdentityOrganizationGeneralSchemas
    User = MaleoIdentityUserGeneralSchemas
    UserProfile = MaleoIdentityUserProfileGeneralSchemas
    UserSystemRole = MaleoIdentityUserSystemRoleGeneralSchemas
    UserOrganization = MaleoIdentityUserOrganizationGeneralSchemas