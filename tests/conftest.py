import os

import pytest
from dotenv import load_dotenv

from supabase_py_async import AsyncClient, create_client


def pytest_configure(config) -> None:
    load_dotenv(dotenv_path="tests/tests.env")


@pytest.fixture(scope="session")
@pytest.mark.asyncio
async def supabase() -> AsyncClient:
    url = os.environ.get("SUPABASE_TEST_URL")
    assert url is not None, "Must provide SUPABASE_TEST_URL environment variable"
    key = os.environ.get("SUPABASE_TEST_KEY")
    assert key is not None, "Must provide SUPABASE_TEST_KEY environment variable"
    return await create_client(url, key)
