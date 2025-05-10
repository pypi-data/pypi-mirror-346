from fastapi import status
from maleo_foundation.managers.client.base import ClientService
from maleo_foundation.utils.exceptions import BaseExceptions
from maleo_identity.client.controllers import MaleoIdentityUserControllers
from maleo_identity.enums.general import MaleoIdentityGeneralEnums
from maleo_identity.models.transfers.parameters.general.user import MaleoIdentityUserGeneralParametersTransfers
from maleo_identity.models.transfers.parameters.client.user import MaleoIdentityUserClientParametersTransfers
from maleo_identity.models.transfers.results.general.user import MaleoIdentityUserGeneralResultsTransfers
from maleo_identity.types.results.general.user import MaleoIdentityUserGeneralResultsTypes

class MaleoIdentityUserClientService(ClientService):
    def __init__(self, logger, controllers:MaleoIdentityUserControllers):
        super().__init__(logger)
        self._controllers = controllers

    @property
    def controllers(self) -> MaleoIdentityUserControllers:
        raise self._controllers

    async def get_users(
        self,
        parameters:MaleoIdentityUserClientParametersTransfers.GetMultiple,
        controller_type:MaleoIdentityGeneralEnums.ClientControllerType = MaleoIdentityGeneralEnums.ClientControllerType.HTTP
    ) -> MaleoIdentityUserGeneralResultsTypes.GetMultiple:
        """Retrieve users from MaleoIdentity"""
        @BaseExceptions.service_exception_handler(
            operation="retrieving users",
            logger=self._logger,
            fail_result_class=MaleoIdentityUserGeneralResultsTransfers.Fail
        )
        async def _impl():
            #* Validate chosen controller type
            if not isinstance(controller_type, MaleoIdentityGeneralEnums.ClientControllerType):
                message = "Invalid controller type"
                description = "The provided controller type did not exists"
                return MaleoIdentityUserGeneralResultsTransfers.Fail(message=message, description=description)
            #* Retrieve users using chosen controller
            if controller_type == MaleoIdentityGeneralEnums.ClientControllerType.HTTP:
                controller_result = await self._controllers.http.get_users(parameters=parameters)
            else:
                message = "Invalid controller type"
                description = "The provided controller type has not been implemented"
                return MaleoIdentityUserGeneralResultsTransfers.Fail(message=message, description=description)
            #* Return proper response
            if not controller_result.success:
                return MaleoIdentityUserGeneralResultsTransfers.Fail.model_validate(controller_result.content)
            else:
                if controller_result.content["data"] is None:
                    return MaleoIdentityUserGeneralResultsTransfers.NoData.model_validate(controller_result.content)
                else:
                    return MaleoIdentityUserGeneralResultsTransfers.MultipleData.model_validate(controller_result.content)
        return await _impl()

    async def get_user(
        self,
        parameters:MaleoIdentityUserGeneralParametersTransfers.GetSingle,
        controller_type:MaleoIdentityGeneralEnums.ClientControllerType = MaleoIdentityGeneralEnums.ClientControllerType.HTTP
    ) -> MaleoIdentityUserGeneralResultsTypes.GetSingle:
        """Retrieve user from MaleoIdentity"""
        @BaseExceptions.service_exception_handler(
            operation="retrieving user",
            logger=self._logger,
            fail_result_class=MaleoIdentityUserGeneralResultsTransfers.Fail
        )
        async def _impl():
            #* Validate chosen controller type
            if not isinstance(controller_type, MaleoIdentityGeneralEnums.ClientControllerType):
                message = "Invalid controller type"
                description = "The provided controller type did not exists"
                return MaleoIdentityUserGeneralResultsTransfers.Fail(message=message, description=description)
            #* Retrieve user using chosen controller
            if controller_type == MaleoIdentityGeneralEnums.ClientControllerType.HTTP:
                controller_result = await self._controllers.http.get_user(parameters=parameters)
            else:
                message = "Invalid controller type"
                description = "The provided controller type has not been implemented"
                return MaleoIdentityUserGeneralResultsTransfers.Fail(message=message, description=description)
            #* Return proper response
            if not controller_result.success:
                if controller_result.status_code != status.HTTP_404_NOT_FOUND:
                    return MaleoIdentityUserGeneralResultsTransfers.Fail.model_validate(controller_result.content)
                else:
                    return MaleoIdentityUserGeneralResultsTransfers.NoData.model_validate(controller_result.content)
            else:
                return MaleoIdentityUserGeneralResultsTransfers.SingleData.model_validate(controller_result.content)
        return await _impl()

    async def create(
        self,
        parameters:MaleoIdentityUserGeneralParametersTransfers.Create,
        controller_type:MaleoIdentityGeneralEnums.ClientControllerType = MaleoIdentityGeneralEnums.ClientControllerType.HTTP
    ) -> MaleoIdentityUserGeneralResultsTypes.CreateOrUpdate:
        """Create a new user in MaleoIdentity"""
        @BaseExceptions.service_exception_handler(
            operation="creating a new user",
            logger=self._logger,
            fail_result_class=MaleoIdentityUserGeneralResultsTransfers.Fail
        )
        async def _impl():
            #* Validate chosen controller type
            if not isinstance(controller_type, MaleoIdentityGeneralEnums.ClientControllerType):
                message = "Invalid controller type"
                description = "The provided controller type did not exists"
                return MaleoIdentityUserGeneralResultsTransfers.Fail(message=message, description=description)
            #* Create a new user using chosen controller
            if controller_type == MaleoIdentityGeneralEnums.ClientControllerType.HTTP:
                controller_result = await self._controllers.http.create(parameters=parameters)
            else:
                message = "Invalid controller type"
                description = "The provided controller type has not been implemented"
                return MaleoIdentityUserGeneralResultsTransfers.Fail(message=message, description=description)
            #* Return proper response
            if not controller_result.success:
                return MaleoIdentityUserGeneralResultsTransfers.NoData.model_validate(controller_result.content)
            else:
                return MaleoIdentityUserGeneralResultsTransfers.SingleData.model_validate(controller_result.content)
        return await _impl()

    async def update(
        self,
        parameters:MaleoIdentityUserGeneralParametersTransfers.Update,
        controller_type:MaleoIdentityGeneralEnums.ClientControllerType = MaleoIdentityGeneralEnums.ClientControllerType.HTTP
    ) -> MaleoIdentityUserGeneralResultsTypes.CreateOrUpdate:
        """Update user's data in MaleoIdentity"""
        @BaseExceptions.service_exception_handler(
            operation="updating user's data",
            logger=self._logger,
            fail_result_class=MaleoIdentityUserGeneralResultsTransfers.Fail
        )
        async def _impl():
            #* Validate chosen controller type
            if not isinstance(controller_type, MaleoIdentityGeneralEnums.ClientControllerType):
                message = "Invalid controller type"
                description = "The provided controller type did not exists"
                return MaleoIdentityUserGeneralResultsTransfers.Fail(message=message, description=description)
            #* Update user's data using chosen controller
            if controller_type == MaleoIdentityGeneralEnums.ClientControllerType.HTTP:
                controller_result = await self._controllers.http.update(parameters=parameters)
            else:
                message = "Invalid controller type"
                description = "The provided controller type has not been implemented"
                return MaleoIdentityUserGeneralResultsTransfers.Fail(message=message, description=description)
            #* Return proper response
            if not controller_result.success:
                return MaleoIdentityUserGeneralResultsTransfers.NoData.model_validate(controller_result.content)
            else:
                return MaleoIdentityUserGeneralResultsTransfers.SingleData.model_validate(controller_result.content)
        return await _impl()