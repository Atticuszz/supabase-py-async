import re
from typing import Any

from gotrue.types import AuthChangeEvent, Session
from httpx import Timeout
from postgrest import AsyncPostgrestClient, AsyncRequestBuilder
from postgrest._async.request_builder import AsyncRPCFilterRequestBuilder
from postgrest.constants import DEFAULT_POSTGREST_CLIENT_TIMEOUT
from storage3 import AsyncStorageClient
from storage3.constants import DEFAULT_TIMEOUT as DEFAULT_STORAGE_CLIENT_TIMEOUT
from supafunc import AsyncFunctionsClient

from .lib.auth_client import AsyncSupabaseAuthClient
from .lib.client_options import ClientOptions


# Create an exception class when user does not provide a valid url or key.
class SupabaseException(Exception):
    def __init__(self, message: str):
        self.message = message
        super().__init__(self.message)


class AsyncClient:
    """Supabase client class."""

    def __init__(
        self,
        supabase_url: str,
        supabase_key: str,
        access_token: str | None = None,
        options: ClientOptions = ClientOptions(),
    ):
        """Instantiate the client.

        Parameters
        ----------
        supabase_url: str
            The URL to the Supabase instance that should be connected to.
        supabase_key: str
            The API key to the Supabase instance that should be connected to.
        **options
            Any extra settings to be optionally specified - also see the
            `DEFAULT_OPTIONS` dict.
        """

        if not supabase_url:
            raise SupabaseException("supabase_url is required")
        if not supabase_key:
            raise SupabaseException("supabase_key is required")

        # Check if the url and key are valid
        if not re.match(r"^(https?)://.+", supabase_url):
            raise SupabaseException("Invalid URL")

        # Check if the key is a valid JWT
        if not re.match(
            r"^[A-Za-z0-9-_=]+\.[A-Za-z0-9-_=]+\.?[A-Za-z0-9-_.+/=]*$", supabase_key
        ):
            raise SupabaseException("Invalid API key")

        self.supabase_url = supabase_url
        self.supabase_key = supabase_key
        # only can be set by init instance
        self._access_token = access_token if access_token else supabase_key
        # will be modified by auth state change
        self._auth_token = self._create_auth_header(self._access_token)

        self.options = options
        # update options headers
        self._update_auth_headers()
        self.rest_url = f"{supabase_url}/rest/v1"
        self.realtime_url = f"{supabase_url}/realtime/v1".replace("http", "ws")
        self.auth_url = f"{supabase_url}/auth/v1"
        self.storage_url = f"{supabase_url}/storage/v1"
        self.functions_url = f"{supabase_url}/functions/v1"
        self.schema = options.schema

        # Instantiate clients.
        self.auth = self._init_supabase_auth_client(
            auth_url=self.auth_url,
            client_options=options,
        )
        # TODO: Bring up to parity with JS client.
        # self.realtime: SupabaseRealtimeClient = self._init_realtime_client(
        #     realtime_url=self.realtime_url,
        #     supabase_key=self.supabase_key,
        # )
        self.realtime = None
        self._postgrest = None
        self._storage = None
        self._functions = None
        self.auth.on_auth_state_change(self._listen_to_auth_events)

    @classmethod
    async def create(
        cls,
        supabase_url: str,
        supabase_key: str,
        access_token: str | None = None,
        options: ClientOptions = ClientOptions(),
    ):
        client = cls(supabase_url, supabase_key, access_token, options)
        return client

    def table(self, table_name: str) -> AsyncRequestBuilder:
        """Perform a table operation.

        Note that the supabase client uses the `from` method, but in Python,
        this is a reserved keyword, so we have elected to use the name `table`.
        Alternatively you can use the `.from_()` method.
        """
        return self.from_(table_name)

    def from_(self, table_name: str) -> AsyncRequestBuilder:
        """Perform a table operation.

        See the `table` method.
        """
        return self.postgrest.from_(table_name)

    def rpc(self, fn: str, params: dict[Any, Any]) -> AsyncRPCFilterRequestBuilder[Any]:
        """Performs a stored procedure call.

        Parameters
        ----------
        fn : callable
            The stored procedure call to be executed.
        params : dict of any
            Parameters passed into the stored procedure call.

        Returns
        -------
        SyncFilterRequestBuilder
            Returns a filter builder. This lets you apply filters on the response
            of an RPC.
        """
        return self.postgrest.rpc(fn, params)

    @property
    def postgrest(self):
        if self._postgrest is None:
            self._update_auth_headers()
            self._postgrest = self._init_postgrest_client(
                rest_url=self.rest_url,
                headers=self.options.headers,
                schema=self.options.schema,
                timeout=self.options.postgrest_client_timeout,
            )

        return self._postgrest

    @property
    def storage(self):
        if self._storage is None:
            self._update_auth_headers()
            self._storage = self._init_storage_client(
                storage_url=self.storage_url,
                headers=self.options.headers,
                storage_client_timeout=self.options.storage_client_timeout,
            )
        return self._storage

    @property
    def functions(self):
        if self._functions is None:
            self._update_auth_headers()
            self._functions = AsyncFunctionsClient(
                self.functions_url, self.options.headers
            )
        return self._functions

    @staticmethod
    def _init_storage_client(
        storage_url: str,
        headers: dict[str, str],
        storage_client_timeout: int = DEFAULT_STORAGE_CLIENT_TIMEOUT,
    ) -> AsyncStorageClient:
        return AsyncStorageClient(storage_url, headers, storage_client_timeout)

    @staticmethod
    def _init_supabase_auth_client(
        auth_url: str,
        client_options: ClientOptions,
    ) -> AsyncSupabaseAuthClient:
        """Creates a wrapped instance of the GoTrue Client."""
        return AsyncSupabaseAuthClient(
            url=auth_url,
            auto_refresh_token=client_options.auto_refresh_token,
            persist_session=client_options.persist_session,
            storage=client_options.storage,
            headers=client_options.headers,
            flow_type=client_options.flow_type,
        )

    @staticmethod
    def _init_postgrest_client(
        rest_url: str,
        headers: dict[str, str],
        schema: str,
        timeout: int | float | Timeout = DEFAULT_POSTGREST_CLIENT_TIMEOUT,
    ) -> AsyncPostgrestClient:
        """Private helper for creating an instance of the Postgrest client."""
        return AsyncPostgrestClient(
            rest_url, headers=headers, schema=schema, timeout=timeout
        )

    def _create_auth_header(self, token: str):
        return {
            "Authorization": f"Bearer {token}",
        }

    async def _get_token_header(self):
        """
        if signed in will return access_token from session
        or return default access_token ,if None, will return supabase_key
        """
        try:
            session = await self.auth.get_session()
            access_token = session.access_token
        except Exception as err:
            access_token = self._access_token
        return self._create_auth_header(access_token)

    def _update_auth_headers(self) -> None:
        """Helper method to get auth headers."""
        new_headers = {
            "apiKey": self.supabase_key,
            **self._auth_token,
        }
        self.options.headers.update(**new_headers)

    def _listen_to_auth_events(self, event: AuthChangeEvent, session: Session | None):
        """listen to auth events and update auth token"""
        access_token = self._access_token
        if event in ["SIGNED_IN", "TOKEN_REFRESHED", "SIGNED_OUT"]:
            # reset postgrest and storage instance on event change
            self._postgrest = None
            self._storage = None
            self._functions = None
            access_token = session.access_token if session else self._access_token
        self._auth_token = self._create_auth_header(access_token)


async def create_client(
    supabase_url: str,
    supabase_key: str,
    access_token: str | None = None,
    options: ClientOptions = ClientOptions(),
) -> AsyncClient:
    """Create client function to instantiate supabase client like JS runtime.

    Parameters
    ----------
    supabase_url: str
        The URL to the Supabase instance that should be connected to.
    supabase_key: str
        The API key to the Supabase instance that should be connected to.
    **options
        Any extra settings to be optionally specified - also see the
        `DEFAULT_OPTIONS` dict.

    Examples
    --------
    Instantiating the client.
    >>> import os
    >>> from supabase_py_async import create_client, AsyncClient
    >>>
    >>> url: str = os.environ.get("SUPABASE_TEST_URL")
    >>> key: str = os.environ.get("SUPABASE_TEST_KEY")
    >>> supabase: AsyncClient = create_client(url, key)

    Returns
    -------
    Client
    """
    return await AsyncClient.create(
        supabase_url=supabase_url,
        supabase_key=supabase_key,
        access_token=access_token,
        options=options,
    )
