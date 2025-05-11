from typing import Awaitable, Union
from .utils.to_async import to_async
from ..metadata import MetadataService
from ...models import DeletionCost, ReallocatePrototype, Status, Token


class MetadataServiceAsync(MetadataService):
    """
    Async Wrapper for MetadataServiceAsync
    """

    def get_deletion_cost(self) -> Awaitable[DeletionCost]:
        return to_async(super().get_deletion_cost)()

    def replace_deletion_cost(
        self, request_body: DeletionCost
    ) -> Awaitable[DeletionCost]:
        return to_async(super().replace_deletion_cost)(request_body)

    def reallocate(self, request_body: ReallocatePrototype) -> Awaitable[None]:
        return to_async(super().reallocate)(request_body)

    def recreate(self) -> Awaitable[None]:
        return to_async(super().recreate)()

    def restart(self) -> Awaitable[None]:
        return to_async(super().restart)()

    def get_status(self) -> Awaitable[Status]:
        return to_async(super().get_status)()

    def get_token(self) -> Awaitable[Token]:
        return to_async(super().get_token)()
