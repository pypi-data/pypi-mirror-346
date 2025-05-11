from typing import Union
from .net.environment import Environment
from .sdk import SaladCloudImdsSdk
from .services.async_.metadata import MetadataServiceAsync


class SaladCloudImdsSdkAsync(SaladCloudImdsSdk):
    """
    SaladCloudImdsSdkAsync is the asynchronous version of the SaladCloudImdsSdk SDK Client.
    """

    def __init__(
        self, base_url: Union[Environment, str, None] = None, timeout: int = 60000
    ):
        super().__init__(base_url=base_url, timeout=timeout)

        self.metadata = MetadataServiceAsync(base_url=self._base_url)
