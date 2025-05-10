from __future__ import annotations
from .organization import OrganizationTransfers
from .user_profile import UserProfileTransfers
from .user import UserTransfers
from .user_system_role import UserSystemRoleTransfers
from .user_organization import UserOrganizationTransfers

class MaleoIdentityGeneralTransfers:
    Organization = OrganizationTransfers
    UserProfile = UserProfileTransfers
    User = UserTransfers
    UserSystemRole = UserSystemRoleTransfers
    UserOrganization = UserOrganizationTransfers