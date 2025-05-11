from .utils.json_map import JsonMap
from .utils.base_model import BaseModel


@JsonMap({})
class Token(BaseModel):
    """The identity token of the current container instance.

    :param jwt: The JSON Web Token (JWT) that may be used to identify the running container. The JWT may be verified using the JSON Web Key Set (JWKS) available at https://matrix-rest-api.salad.com/.well-known/workload-jwks.json.
    :type jwt: str
    """

    def __init__(self, jwt: str, **kwargs):
        """The identity token of the current container instance.

        :param jwt: The JSON Web Token (JWT) that may be used to identify the running container. The JWT may be verified using the JSON Web Key Set (JWKS) available at https://matrix-rest-api.salad.com/.well-known/workload-jwks.json.
        :type jwt: str
        """
        self.jwt = self._define_str("jwt", jwt, min_length=1, max_length=1000)
        self._kwargs = kwargs
