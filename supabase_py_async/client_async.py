# coding=utf-8
import re
from typing import Any, Dict, Union

from aiohttp import ClientTimeout as Timeout
from deprecation import deprecated
from gotrue.errors import AuthSessionMissingError
from gotrue.types import AuthChangeEvent, AuthResponse
# from postgrest import SyncFilterRequestBuilder, SyncPostgrestClient, SyncRequestBuilder
# 我们假设这些都是异步库的版本
from postgrest import AsyncPostgrestClient, AsyncRequestBuilder
from postgrest._async.request_builder import AsyncRPCFilterRequestBuilder
# from gotrue.types import AsyncSupabaseAuthClient
from postgrest.constants import DEFAULT_POSTGREST_CLIENT_TIMEOUT
from storage3.constants import DEFAULT_TIMEOUT as DEFAULT_STORAGE_CLIENT_TIMEOUT
from supafunc import AsyncFunctionsClient

from .lib.auth_client import SupabaseAuthClient
from .lib.client_options import ClientOptions
from .lib.storage_client import SupabaseStorageClient
from .types import Session

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
                r"^[A-Za-z0-9-_=]+\.[A-Za-z0-9-_=]+\.?[A-Za-z0-9-_.+/=]*$",
                supabase_key):
            raise SupabaseException("Invalid API key")

        self.supabase_url = supabase_url
        self.supabase_key = supabase_key
        options.headers.update(self._get_auth_headers())
        self.options = options
        self.rest_url = f"{supabase_url}/rest/v1"
        self.realtime_url = f"{supabase_url}/realtime/v1".replace("http", "ws")
        self.auth_url = f"{supabase_url}/auth/v1"
        self.storage_url = f"{supabase_url}/storage/v1"
        self.functions_url = f"{supabase_url}/functions/v1"
        self.schema = options.schema
        # Instantiate clients.
        self.auth = self._init_supabase_auth_client(
            auth_url=self.auth_url,
            client_options=self.options,
        )
        self.auth_clients: dict[str, SupabaseAuthClient] = {}
        # TODO: Bring up to parity with JS client.
        # self.realtime: SupabaseRealtimeClient = self._init_realtime_client(
        #     realtime_url=self.realtime_url,
        #     supabase_key=self.supabase_key,
        # )
        # removed in 2.0.4
        # self.auth.on_auth_state_change(self._listen_to_auth_events)

    #     add to single async function to start up listeners

    async def add_auth_clients(self, auth_response: AuthResponse):
        """
        >>> auth_response:AuthResponse = await self.auth.sign_in_with_password({"email":ur_email, "password":ur_password)
        #  or other sign in methods
        >>> await supabase.add_auth_clients(auth_response)
        # next time your can use operation with supabase like this,i assume you get a user access_token
        >>> auth_client = await self.update_auth_session(auth_response.seesion.access_token)
        >>> await self.table("ur_table_name",auth_client).select("*").execute()
        """
        # create a new auth client for the user
        # use auth key to sign in and update token header for different roles
        options = ClientOptions(
            headers=self._get_token_header(
                auth_response.session.access_token))

        auth_client: SupabaseAuthClient = self._init_supabase_auth_client(
            auth_url=self.auth_url,
            client_options=self.options,
        )

        session: Session | None = await auth_client.get_session()
        if session is None:
            # you should catch it and do something
            raise AuthSessionMissingError
        # update auth in header
        auth_client.options.headers.update(self._get_token_header(session.access_token))
        self.auth_clients[auth_response.session.access_token] = auth_client

    async def update_auth_session(self, auth_token: str) -> SupabaseAuthClient:
        """
        every operation should call this function to get new auth token
        update auth token
        exception:AuthSessionMissingError which means auth session has expired or log out or have not log in or do not exist
        """
        auth_client: SupabaseAuthClient = self.auth_clients[auth_token]
        # get session function have consider all stuffs like refresh
        # token,expired...
        session: Session | None = await auth_client.get_session()
        new_token = session.access_token
        if session is None:
            del self.auth_clients[auth_token]
            # you should catch it and do something
            raise AuthSessionMissingError
        elif new_token != auth_token:
            # update auth_client client
            auth_client.options.headers.update(self._get_token_header(new_token))
            del self.auth_clients[auth_token]
            self.auth_clients[new_token] = self._init_supabase_auth_client(
                auth_url=self.auth_url,
                client_options=auth_client.options,
            )
        return self.auth_clients[new_token]

    async def schedue_check_auth_session(self, auth_token: str):
        """
        check auth session and refresh token
        """
        pass

    def table(
            self,
            table_name: str,
            auth_client: SupabaseAuthClient) -> AsyncRequestBuilder:
        """Perform a table operation.

        Note that the supabase client uses the `from` method, but in Python,
        this is a reserved keyword, so we have elected to use the name `table`.
        Alternatively you can use the `.from_()` method.
        """
        postgrest = self._init_postgrest_client(
            rest_url=self.rest_url,
            headers=auth_client.options.headers,
            schema=auth_client.options.schema,
            timeout=auth_client.options.postgrest_client_timeout,
        )
        return postgrest.from_(table_name)

    def rpc(self,
            fn: str,
            params: Dict[Any, Any],
            auth_client: SupabaseAuthClient) -> AsyncRPCFilterRequestBuilder[Any]:
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
        postgrest = self._init_postgrest_client(
            rest_url=self.rest_url,
            headers=auth_client.options.headers,
            schema=auth_client.options.schema,
            timeout=auth_client.options.postgrest_client_timeout,
        )
        return postgrest.rpc(fn, params)

    def storage(
            self,
            auth_client: SupabaseAuthClient) -> SupabaseStorageClient:
        """Returns a storage client."""
        storage = self._init_storage_client(
            storage_url=self.storage_url,
            headers=auth_client.options.headers,
            storage_client_timeout=auth_client.options.storage_client_timeout,
        )
        return storage

    def functions(
            self,
            auth_client: SupabaseAuthClient) -> AsyncFunctionsClient:
        functions = AsyncFunctionsClient(
            self.functions_url, auth_client.options.headers)
        return functions

    #     async def remove_subscription_helper(resolve):
    #         try:
    #             await self._close_subscription(subscription)
    #             open_subscriptions = len(self.get_subscriptions())
    #             if not open_subscriptions:
    #                 error = await self.realtime.disconnect()
    #                 if error:
    #                     return {"error": None, "data": { open_subscriptions}}
    #         except Exception as e:
    #             raise e
    #     return remove_subscription_helper(subscription)

    # async def _close_subscription(self, subscription):
    #    """Close a given subscription

    #    Parameters
    #    ----------
    #    subscription
    #        The name of the channel
    #    """
    #    if not subscription.closed:
    #        await self._closeChannel(subscription)

    # def get_subscriptions(self):
    #     """Return all channels the client is subscribed to."""
    #     return self.realtime.channels

    # @staticmethod
    # def _init_realtime_client(
    #     realtime_url: str, supabase_key: str
    # ) -> SupabaseRealtimeClient:
    #     """Private method for creating an instance of the realtime-py client."""
    #     return SupabaseRealtimeClient(
    #         realtime_url, {"params": {"apikey": supabase_key}}
    #     )
    @staticmethod
    def _init_storage_client(
            storage_url: str,
            headers: Dict[str, str],
            storage_client_timeout: int = DEFAULT_STORAGE_CLIENT_TIMEOUT,
    ) -> SupabaseStorageClient:
        return SupabaseStorageClient(
            storage_url, headers, storage_client_timeout)

    @staticmethod
    def _init_supabase_auth_client(
            auth_url: str,
            client_options: ClientOptions,
    ) -> SupabaseAuthClient:
        """Creates a wrapped instance of the GoTrue Client."""
        return SupabaseAuthClient(
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
            headers: Dict[str, str],
            schema: str,
            timeout: Union[int, float, Timeout] = DEFAULT_POSTGREST_CLIENT_TIMEOUT,
    ) -> AsyncPostgrestClient:
        """Private helper for creating an instance of the Postgrest client."""
        return AsyncPostgrestClient(
            rest_url, headers=headers, schema=schema, timeout=timeout
        )

    def _get_auth_headers(self) -> Dict[str, str]:
        """Helper method to get auth headers."""
        # What's the corresponding method to get the token
        return {
            "apiKey": self.supabase_key,
            "Authorization": f"Bearer {self.supabase_key}",
        }

    def _get_token_header(self, access_token: str |
                                              None = None) -> Dict[str, str]:
        """Helper method to get and verify token header."""
        access_token = access_token if access_token else self.supabase_key
        return {
            "Authorization": f"Bearer {access_token}",
        }

    def _listen_to_auth_events(self, event: AuthChangeEvent):
        if event in ["SIGNED_IN", "TOKEN_REFRESHED", "SIGNED_OUT"]:
            # reset postgrest and storage instance on event change
            self._postgrest = None
            self._storage = None
            self._functions = None


def create_client(
        supabase_url: str,
        supabase_key: str,
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
    >>> supabase: AsyncClient =  create_client(url, key)

    Returns
    -------
    Client
    """
    return AsyncClient(
        supabase_url=supabase_url,
        supabase_key=supabase_key,
        options=options)
