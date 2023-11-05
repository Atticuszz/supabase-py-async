import pytest
from gotrue import AsyncMemoryStorage

from supabase_py_async.lib.client_options import ClientOptions


class TestClientOptions:
    @pytest.mark.asyncio
    async def test_replace_returns_updated_options(self):
        storage = AsyncMemoryStorage()
        await storage.set_item("key", "value")
        options = ClientOptions(
            schema="schema",
            headers={"key": "value"},
            auto_refresh_token=False,
            persist_session=False,
            storage=storage,
            realtime={"key": "value"},
        )

        actual = options.replace(schema="new schema")
        expected = ClientOptions(
            schema="new schema",
            headers={"key": "value"},
            auto_refresh_token=False,
            persist_session=False,
            storage=storage,
            realtime={"key": "value"},
        )

        assert actual == expected

    @pytest.mark.asyncio
    async def test_replace_updates_only_new_options(self):
        # Arrange
        storage = AsyncMemoryStorage()
        await storage.set_item("key", "value")
        options = ClientOptions(storage=storage)
        new_options = options.replace()

        # Act
        await new_options.storage.set_item("key", "new_value")

        # Assert
        assert await options.storage.get_item("key") == "new_value"
        assert await new_options.storage.get_item("key") == "new_value"
