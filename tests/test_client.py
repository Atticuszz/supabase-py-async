from typing import Any

import pytest


@pytest.mark.xfail(
    reason="None of these values should be able to instantiate a client object"
)
@pytest.mark.parametrize("url", ["", None, "valeefgpoqwjgpj", 139, -1, {}, []])
@pytest.mark.parametrize("key", ["", None, "valeefgpoqwjgpj", 139, -1, {}, []])
@pytest.mark.asyncio
async def test_incorrect_values_dont_instantiate_client(url: Any, key: Any) -> None:
    """Ensure we can't instantiate client with invalid values."""
    from supabase_py_async import AsyncClient, create_client

    _: AsyncClient = await create_client(url, key)
