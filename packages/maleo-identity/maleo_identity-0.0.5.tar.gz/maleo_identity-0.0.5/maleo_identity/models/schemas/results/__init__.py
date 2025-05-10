from __future__ import annotations
from .organization import MaleoIdentityOrganizationResultsSchemas
from .user import MaleoIdentityUserResultsSchemas
from .user_profile import MaleoIdentityUserProfileResultsSchemas
from .user_system_role import MaleoIdentityUserSystemRoleResultsSchemas
from .user_organization import MaleoIdentityUserOrganizationResultsSchemas

class MaleoIdentityResultsSchemas:
    Organization = MaleoIdentityOrganizationResultsSchemas
    User = MaleoIdentityUserResultsSchemas
    UserProfile = MaleoIdentityUserProfileResultsSchemas
    UserSystemRole = MaleoIdentityUserSystemRoleResultsSchemas
    UserOrganization = MaleoIdentityUserOrganizationResultsSchemas