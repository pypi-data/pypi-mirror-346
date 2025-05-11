from .utils.json_map import JsonMap
from .utils.base_model import BaseModel


@JsonMap({})
class DeletionCost(BaseModel):
    """The deletion cost of the current container instance.

    :param deletion_cost: An integer value that identifies the relative cost to the application running across the container group if the current container instance is deleted. A higher value indicates a higher cost, and a lower value indicates a lower cost. If the container group is scaled down, the scheduler will attempt to delete the container instances with the lowest deletion costs first.
    :type deletion_cost: int
    """

    def __init__(self, deletion_cost: int, **kwargs):
        """The deletion cost of the current container instance.

        :param deletion_cost: An integer value that identifies the relative cost to the application running across the container group if the current container instance is deleted. A higher value indicates a higher cost, and a lower value indicates a lower cost. If the container group is scaled down, the scheduler will attempt to delete the container instances with the lowest deletion costs first.
        :type deletion_cost: int
        """
        self.deletion_cost = self._define_number(
            "deletion_cost", deletion_cost, ge=-2147483648, le=2147483647
        )
        self._kwargs = kwargs
