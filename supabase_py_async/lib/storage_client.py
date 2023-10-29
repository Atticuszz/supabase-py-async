from deprecation import deprecated
from storage3 import AsyncStorageClient
from storage3._async.file_api import AsyncBucketProxy


class SupabaseStorageClient(AsyncStorageClient):
    """Manage storage buckets and files."""

    @deprecated("0.5.4", "0.6.0", details="Use `.from_()` instead")
    def StorageFileAPI(self, id_: str) -> AsyncBucketProxy:
        return super().from_(id_)
