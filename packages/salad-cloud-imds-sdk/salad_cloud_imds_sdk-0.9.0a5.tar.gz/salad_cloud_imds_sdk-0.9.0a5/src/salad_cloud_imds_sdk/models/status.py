from .utils.json_map import JsonMap
from .utils.base_model import BaseModel


@JsonMap({})
class Status(BaseModel):
    """The health statuses of the current container instance.

    :param ready: `true` if the running container is ready. If a readiness probe is defined, this returns the latest result of the probe. If a readiness probe is not defined but a startup probe is defined, this returns the same value as the `started` property. If neither a readiness probe nor a startup probe are defined, returns `true`.
    :type ready: bool
    :param started: `true` if the running container is started. If a startup probe is defined, this returns the latest result of the probe. If a startup probe is not defined, returns `true`.
    :type started: bool
    """

    def __init__(self, ready: bool, started: bool, **kwargs):
        """The health statuses of the current container instance.

        :param ready: `true` if the running container is ready. If a readiness probe is defined, this returns the latest result of the probe. If a readiness probe is not defined but a startup probe is defined, this returns the same value as the `started` property. If neither a readiness probe nor a startup probe are defined, returns `true`.
        :type ready: bool
        :param started: `true` if the running container is started. If a startup probe is defined, this returns the latest result of the probe. If a startup probe is not defined, returns `true`.
        :type started: bool
        """
        self.ready = ready
        self.started = started
        self._kwargs = kwargs
