from .utils.json_map import JsonMap
from .utils.base_model import BaseModel


@JsonMap({})
class ReallocatePrototype(BaseModel):
    """Represents a request to reallocate the current container instance to another SaladCloud node.

    :param reason: The reason for reallocating the current container instance. This value is reported to SaladCloud support for quality assurance purposes of SaladCloud nodes.
    :type reason: str
    """

    def __init__(self, reason: str, **kwargs):
        """Represents a request to reallocate the current container instance to another SaladCloud node.

        :param reason: The reason for reallocating the current container instance. This value is reported to SaladCloud support for quality assurance purposes of SaladCloud nodes.
        :type reason: str
        """
        self.reason = self._define_str("reason", reason, min_length=1, max_length=1000)
        self._kwargs = kwargs
