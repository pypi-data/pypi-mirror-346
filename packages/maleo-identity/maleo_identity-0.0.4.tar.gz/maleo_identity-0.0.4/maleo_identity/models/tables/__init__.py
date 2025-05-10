from __future__ import annotations
from .organization import OrganizationsTable
from .user import UsersTable
from .user_profile import UserProfilesTable
from .user_system_role import UserSystemRolesTable
from .user_organization import UserOrganizationsTable

class MaleoIdentityTables:
    Organization = OrganizationsTable
    User = UsersTable
    UserProfile = UserProfilesTable
    UserSystemRole = UserSystemRolesTable
    UserOrganization = UserOrganizationsTable