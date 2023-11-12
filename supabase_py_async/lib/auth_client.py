from typing import Dict, Optional

# from httpx import AsyncClient as BaseClient
from aiohttp import ClientSession as BaseClient
from gotrue import AuthFlowType, AsyncGoTrueClient, AsyncMemoryStorage, AsyncSupportedStorage

from .client_options import ClientOptions


# TODO -ClientSession is not a good choice for AsyncClient inheritance
class AsyncClient(BaseClient):
    def aclose(self) -> None:
        self.close()


class SupabaseAuthClient(AsyncGoTrueClient):
    """SupabaseAuthClient"""

    def __init__(
            self,
            *,
            url: str,
            headers: Optional[Dict[str, str]] = None,
            storage_key: Optional[str] = None,
            auto_refresh_token: bool = True,
            persist_session: bool = True,
            storage: AsyncSupportedStorage = AsyncMemoryStorage(),
            http_client: Optional[AsyncClient] = None,
            flow_type: AuthFlowType = "implicit"
    ):
        """Instantiate SupabaseAuthClient instance."""
        if headers is None:
            headers = {}
        self.options = ClientOptions(
            auto_refresh_token=auto_refresh_token,
            persist_session=persist_session,
            storage=storage,
            headers=headers,
            flow_type=flow_type,
        )
        super().__init__(
            url=url,
            headers=headers,
            storage_key=storage_key,
            auto_refresh_token=auto_refresh_token,
            persist_session=persist_session,
            storage=storage,
            http_client=http_client,
            flow_type=flow_type,
        )
