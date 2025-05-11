from typing import Union
from .utils.validator import Validator
from .utils.base_service import BaseService
from ..net.transport.serializer import Serializer
from ..net.environment.environment import Environment
from ..models.utils.cast_models import cast_models
from ..models import (
    DeletionCost,
    ReallocatePrototype,
    SaladCloudImdsError,
    Status,
    Token,
)


class MetadataService(BaseService):

    @cast_models
    def get_deletion_cost(self) -> DeletionCost:
        """Gets the deletion cost of the current container instance

        ...
        :raises RequestError: Raised when a request fails, with optional HTTP status code and details.
        ...
        :return: The parsed response data.
        :rtype: DeletionCost
        """

        serialized_request = (
            Serializer(
                f"{self.base_url or Environment.DEFAULT.url}/v1/deletion-cost",
            )
            .add_error(403, SaladCloudImdsError)
            .add_error(404, SaladCloudImdsError)
            .serialize()
            .set_method("GET")
        )

        response, status, content = self.send_request(serialized_request)
        return DeletionCost._unmap(response)

    @cast_models
    def replace_deletion_cost(self, request_body: DeletionCost) -> DeletionCost:
        """Replaces the deletion cost of the current container instance

        :param request_body: The request body.
        :type request_body: DeletionCost
        ...
        :raises RequestError: Raised when a request fails, with optional HTTP status code and details.
        ...
        :return: The parsed response data.
        :rtype: DeletionCost
        """

        Validator(DeletionCost).validate(request_body)

        serialized_request = (
            Serializer(
                f"{self.base_url or Environment.DEFAULT.url}/v1/deletion-cost",
            )
            .add_error(400, SaladCloudImdsError)
            .add_error(403, SaladCloudImdsError)
            .add_error(404, SaladCloudImdsError)
            .serialize()
            .set_method("PUT")
            .set_body(request_body)
        )

        response, status, content = self.send_request(serialized_request)
        return DeletionCost._unmap(response)

    @cast_models
    def reallocate(self, request_body: ReallocatePrototype) -> None:
        """Reallocates the current container instance to another SaladCloud node

        :param request_body: The request body.
        :type request_body: ReallocatePrototype
        ...
        :raises RequestError: Raised when a request fails, with optional HTTP status code and details.
        ...
        :return: The parsed response data.
        :rtype: None
        """

        Validator(ReallocatePrototype).validate(request_body)

        serialized_request = (
            Serializer(
                f"{self.base_url or Environment.DEFAULT.url}/v1/reallocate",
            )
            .add_error(400, SaladCloudImdsError)
            .add_error(403, SaladCloudImdsError)
            .add_error(404, SaladCloudImdsError)
            .serialize()
            .set_method("POST")
            .set_body(request_body)
        )

        response, status, content = self.send_request(serialized_request)

    @cast_models
    def recreate(self) -> None:
        """Recreates the current container instance on the same SaladCloud node

        ...
        :raises RequestError: Raised when a request fails, with optional HTTP status code and details.
        ...
        :return: The parsed response data.
        :rtype: None
        """

        serialized_request = (
            Serializer(
                f"{self.base_url or Environment.DEFAULT.url}/v1/recreate",
            )
            .add_error(400, SaladCloudImdsError)
            .add_error(403, SaladCloudImdsError)
            .add_error(404, SaladCloudImdsError)
            .serialize()
            .set_method("POST")
        )

        response, status, content = self.send_request(serialized_request)

    @cast_models
    def restart(self) -> None:
        """Restarts the current container instance on the same SaladCloud node

        ...
        :raises RequestError: Raised when a request fails, with optional HTTP status code and details.
        ...
        :return: The parsed response data.
        :rtype: None
        """

        serialized_request = (
            Serializer(
                f"{self.base_url or Environment.DEFAULT.url}/v1/restart",
            )
            .add_error(400, SaladCloudImdsError)
            .add_error(403, SaladCloudImdsError)
            .add_error(404, SaladCloudImdsError)
            .serialize()
            .set_method("POST")
        )

        response, status, content = self.send_request(serialized_request)

    @cast_models
    def get_status(self) -> Status:
        """Gets the health statuses of the current container instance

        ...
        :raises RequestError: Raised when a request fails, with optional HTTP status code and details.
        ...
        :return: The parsed response data.
        :rtype: Status
        """

        serialized_request = (
            Serializer(
                f"{self.base_url or Environment.DEFAULT.url}/v1/status",
            )
            .add_error(403, SaladCloudImdsError)
            .add_error(404, SaladCloudImdsError)
            .serialize()
            .set_method("GET")
        )

        response, status, content = self.send_request(serialized_request)
        return Status._unmap(response)

    @cast_models
    def get_token(self) -> Token:
        """Gets the identity token of the current container instance

        ...
        :raises RequestError: Raised when a request fails, with optional HTTP status code and details.
        ...
        :return: The parsed response data.
        :rtype: Token
        """

        serialized_request = (
            Serializer(
                f"{self.base_url or Environment.DEFAULT.url}/v1/token",
            )
            .add_error(403, SaladCloudImdsError)
            .add_error(404, SaladCloudImdsError)
            .serialize()
            .set_method("GET")
        )

        response, status, content = self.send_request(serialized_request)
        return Token._unmap(response)
