"""
-*- coding: utf-8 -*-
@Organization : SupaVision
@Author       : 18317
@Date Created : 06/01/2024
@Description  :
"""
import os

from dotenv import load_dotenv
from faker import Faker

from supabase_py_async import AsyncClient, create_client

load_dotenv()


class TestBaseClient:
    url: str = os.getenv("SUPABASE_TEST_URL")
    key: str = os.getenv("SUPABASE_TEST_KEY")
    client: AsyncClient = None
    fake_data = Faker()

    async def superuser_sign_in(self):
        self.client = await create_client(self.url, self.key)
        response = await self.client.auth.sign_in_with_password(
            {"email": "zhouge1831@gmail.com", "password": "Zz030327#"}
        )
        return response
