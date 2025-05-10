from maleo_foundation.managers.client.base import BearerAuth
from maleo_foundation.managers.client.maleo import MaleoClientHTTPController
from maleo_foundation.models.transfers.results.client.controllers.http import BaseClientHTTPControllerResults
from maleo_identity.models.transfers.parameters.general.organization import MaleoIdentityOrganizationGeneralParametersTransfers
from maleo_identity.models.transfers.parameters.client.organization import MaleoIdentityOrganizationClientParametersTransfers

class MaleoIdentityOrganizationHTTPController(MaleoClientHTTPController):
    async def get_organizations(self, parameters:MaleoIdentityOrganizationClientParametersTransfers.GetMultiple) -> BaseClientHTTPControllerResults:
        """Fetch organizations from MaleoIdentity"""
        async with self._manager.get_client() as client:
            #* Define URL
            url = f"{self._manager.url.api}/v1/organizations/"

            #* Parse parameters to query params
            params = MaleoIdentityOrganizationClientParametersTransfers.GetMultipleQuery.model_validate(parameters.model_dump()).model_dump(exclude={"sort_columns", "date_filters"}, exclude_none=True)

            #* Create auth
            auth = BearerAuth(token=self._service_manager.token)

            #* Send request and wait for response
            response = await client.get(url=url, params=params, auth=auth)
            return BaseClientHTTPControllerResults(response=response)

    async def get_organization(self, parameters:MaleoIdentityOrganizationGeneralParametersTransfers.GetSingle) -> BaseClientHTTPControllerResults:
        """Fetch organization from MaleoIdentity"""
        async with self._manager.get_client() as client:
            #* Define URL
            url = f"{self._manager.url.api}/v1/organizations/{parameters.identifier}/{parameters.value}"

            #* Parse parameters to query params
            params = MaleoIdentityOrganizationGeneralParametersTransfers.GetSingleQuery.model_validate(parameters.model_dump()).model_dump(exclude_none=True)

            #* Create auth
            auth = BearerAuth(token=self._service_manager.token)

            #* Send request and wait for response
            response = await client.get(url=url, params=params, auth=auth)
            return BaseClientHTTPControllerResults(response=response)

    async def create(self, parameters:MaleoIdentityOrganizationGeneralParametersTransfers.Create) -> BaseClientHTTPControllerResults:
        """Create a new organization in MaleoIdentity"""
        async with self._manager.get_client() as client:
            #* Define URL
            url = f"{self._manager.url.api}/v1/organizations/"

            #* Declare body
            json = MaleoIdentityOrganizationGeneralParametersTransfers.CreateOrUpdateData.model_validate(parameters.model_dump()).model_dump()

            #* Parse parameters to query params
            params = MaleoIdentityOrganizationGeneralParametersTransfers.CreateOrUpdateQuery.model_validate(parameters.model_dump()).model_dump(exclude_none=True)

            #* Create auth
            auth = BearerAuth(token=self._service_manager.token)

            #* Send request and wait for response
            response = await client.post(url=url, json=json, params=params, auth=auth)
            return BaseClientHTTPControllerResults(response=response)

    async def update(self, parameters:MaleoIdentityOrganizationGeneralParametersTransfers.Update) -> BaseClientHTTPControllerResults:
        """Update organization's data in MaleoIdentity"""
        async with self._manager.get_client() as client:
            #* Define URL
            url = f"{self._manager.url.api}/v1/organizations/{parameters.identifier}/{parameters.value}"

            #* Declare body
            json = MaleoIdentityOrganizationGeneralParametersTransfers.CreateOrUpdateData.model_validate(parameters.model_dump()).model_dump()

            #* Parse parameters to query params
            params = MaleoIdentityOrganizationGeneralParametersTransfers.CreateOrUpdateQuery.model_validate(parameters.model_dump()).model_dump(exclude_none=True)

            #* Create auth
            auth = BearerAuth(token=self._service_manager.token)

            #* Send request and wait for response
            response = await client.put(url=url, json=json, params=params, auth=auth)
            return BaseClientHTTPControllerResults(response=response)