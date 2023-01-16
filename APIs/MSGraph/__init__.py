import adal
import logging


class MSGraphError(Exception):
    """Error for MSGraph issues"""


class MSGraph:
    def __init__(self, token: dict = None, content_type: str = "application/json"):
        self.logger = logging.getLogger(__file__)
        self.token = token
        self.content_type = content_type.strip()
        self.graph_api_endpoint = "https://graph.microsoft.com{0}"
        self.authority = "https://login.microsoftonline.com/"
        self.resource = "https://graph.microsoft.com"
        self.headers = {
            "User-Agent": "python/1.0",
            "Authorization": "Bearer {0}",
            "Accept": "application/json",
            "Content-Type": self.content_type,
        }
        self.tenant_id = None
        self.client_id = None
        self.client_secret = None
        self.set_headers(token)

    def set_headers(self, token):
        if token:
            self.headers["Authorization"] = "Bearer {0}".format(
                self.token["accessToken"]
            )

    def authenticate(
        self,
        tenant: str,
        client_id: str,
        client_secret: str,
        user_name: str,
        user_password: str,
    ):
        """Alias keyword for Get Auth Token.

        For cases where there is no need to get
        token and naming is more suitable.

        :param tenant: [description]
        :param client_id: [description]
        :param client_secret: [description]
        :param user_name: [description]
        :param user_password: [description]
        """
        self.get_auth_token(tenant, client_id, client_secret, user_name, user_password)

    def get_auth_token(
        self,
        tenant: str,
        client_id: str,
        client_secret: str,
        user_name: str,
        user_password: str,
    ):
        token = None
        try:
            self.tenant = tenant.strip()
            self.client_id = client_id.strip()
            self.client_secret = client_secret.strip()
            user_name = user_name.strip()
            user_password = user_password.strip()
            token = self._get_token(user_name, user_password)
            self.set_headers(token)

        except Exception as ex:
            raise ex
        return token

    def _get_token(self, user_name: str, password: str):
        try:
            context = adal.AuthenticationContext(self.authority + self.tenant)
            token = context.acquire_token_with_username_password(
                self.resource, user_name, password, self.client_id
            )
            self.token = token
            return token
        except Exception as e:
            raise e

    def refresh_token(self, refresh_token: str):
        context = adal.AuthenticationContext(self.authority + self.tenant)
        self.token = context.acquire_token_with_refresh_token(
            refresh_token, self.client_id, self.resource, self.client_secret
        )
