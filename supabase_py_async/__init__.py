from .client_async import AsyncClient, create_client
from .lib.auth_client import AsyncSupabaseAuthClient as SupabaseAuthClient
from .lib.realtime_client import SupabaseRealtimeClient

__version__ = "2.3.1"
DEFAULT_HEADERS = {"X-Client-Info": f"supabase-py/{__version__}"}
