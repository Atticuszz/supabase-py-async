from postgrest import APIError as PostgrestAPIError
from postgrest import APIResponse as PostgrestAPIResponse
from storage3.utils import StorageException

from .__version__ import __version__
from .client_async import AsyncClient
from .client_async import AsyncStorageClient as SupabaseStorageClient
from .client_async import ClientOptions, create_client
from .lib.auth_client import AsyncSupabaseAuthClient as SupabaseAuthClient
from .lib.realtime_client import SupabaseRealtimeClient

__all__ = [
    "create_client",
    "AsyncClient",
    "SupabaseAuthClient",
    "SupabaseStorageClient",
    "SupabaseRealtimeClient",
    "PostgrestAPIError",
    "PostgrestAPIResponse",
    "StorageException",
    "__version__",
]
