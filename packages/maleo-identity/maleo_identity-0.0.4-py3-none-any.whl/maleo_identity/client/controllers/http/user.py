from maleo_foundation.managers.client.base import BearerAuth
from maleo_foundation.managers.client.maleo import MaleoClientHTTPController
from maleo_foundation.models.transfers.results.client.controllers.http import BaseClientHTTPControllerResults
from maleo_identity.models.transfers.parameters.general.user import MaleoIdentityUserGeneralParametersTransfers
from maleo_identity.models.transfers.parameters.client.user import MaleoIdentityUserClientParametersTransfers

class MaleoIdentityUserHTTPController(MaleoClientHTTPController):
    async def get_users(self, parameters:MaleoIdentityUserClientParametersTransfers.GetMultiple) -> BaseClientHTTPControllerResults:
        """Fetch users from MaleoIdentity"""
        async with self._manager.get_client() as client:
            #* Define URL
            url = f"{self._manager.url.api}/v1/users/"

            #* Parse parameters to query params
            params = MaleoIdentityUserClientParametersTransfers.GetMultipleQuery.model_validate(parameters.model_dump()).model_dump(exclude={"sort_columns", "date_filters"}, exclude_none=True)

            #* Create auth
            auth = BearerAuth(token=self._service_manager.token)

            #* Send request and wait for response
            response = await client.get(url=url, params=params, auth=auth)
            return BaseClientHTTPControllerResults(response=response)

    async def get_user(self, parameters:MaleoIdentityUserGeneralParametersTransfers.GetSingle) -> BaseClientHTTPControllerResults:
        """Fetch user from MaleoIdentity"""
        async with self._manager.get_client() as client:
            #* Define URL
            url = f"{self._manager.url.api}/v1/users/{parameters.identifier}/{parameters.value}"

            #* Parse parameters to query params
            params = MaleoIdentityUserGeneralParametersTransfers.GetSingleQuery.model_validate(parameters.model_dump()).model_dump(exclude_none=True)

            #* Create auth
            auth = BearerAuth(token=self._service_manager.token)

            #* Send request and wait for response
            response = await client.get(url=url, params=params, auth=auth)
            return BaseClientHTTPControllerResults(response=response)

    async def create(self, parameters:MaleoIdentityUserGeneralParametersTransfers.Create) -> BaseClientHTTPControllerResults:
        """Create a new user in MaleoIdentity"""
        async with self._manager.get_client() as client:
            #* Define URL
            url = f"{self._manager.url.api}/v1/users/"

            #* Declare body
            json = MaleoIdentityUserGeneralParametersTransfers.CreateData.model_validate(parameters.model_dump()).model_dump()

            #* Parse parameters to query params
            params = MaleoIdentityUserGeneralParametersTransfers.CreateOrUpdateQuery.model_validate(parameters.model_dump()).model_dump(exclude_none=True)

            #* Create auth
            auth = BearerAuth(token=self._service_manager.token)

            #* Send request and wait for response
            response = await client.post(url=url, json=json, params=params, auth=auth)
            return BaseClientHTTPControllerResults(response=response)

    async def update(self, parameters:MaleoIdentityUserGeneralParametersTransfers.Update) -> BaseClientHTTPControllerResults:
        """Update user's data in MaleoIdentity"""
        async with self._manager.get_client() as client:
            #* Define URL
            url = f"{self._manager.url.api}/v1/users/{parameters.identifier}/{parameters.value}"

            #* Declare body
            json = MaleoIdentityUserGeneralParametersTransfers.UpdateData.model_validate(parameters.model_dump()).model_dump()

            #* Parse parameters to query params
            params = MaleoIdentityUserGeneralParametersTransfers.CreateOrUpdateQuery.model_validate(parameters.model_dump()).model_dump(exclude_none=True)

            #* Create auth
            auth = BearerAuth(token=self._service_manager.token)

            #* Send request and wait for response
            response = await client.put(url=url, json=json, params=params, auth=auth)
            return BaseClientHTTPControllerResults(response=response)