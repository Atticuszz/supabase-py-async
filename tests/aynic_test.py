# coding=utf-8
import asyncio
import os
import pytest
from dotenv import load_dotenv
from supabase_py_async import create_client

load_dotenv()


@pytest.mark.asyncio
async def test():
    # 获取test.env中的环境变量
    url = os.getenv("SUPABASE_TEST_URL")
    key = os.getenv("SUPABASE_TEST_KEY")
    # 创建客户端
    client = create_client(url, key)
    response = await client.table("task_done_list").select("*").execute()
    print(response.data)
