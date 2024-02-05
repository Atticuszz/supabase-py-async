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
    """base client for test"""

    url: str = os.getenv("SUPABASE_TEST_URL")
    key: str = os.getenv("SUPABASE_TEST_KEY")
    client: AsyncClient = None
    fake_data = Faker()

    async def superuser_sign_in(self):
        self.client = await create_client(self.url, self.key)
        response = await self.client.auth.sign_in_with_password(
            {"email": "zhouge1831@gmail.com", "password": "Zz030327#"}
        )
        assert (
            response.session.access_token
            == self.client._auth_token["Authorization"].split("Bearer ")[1]
        ), "access_token is not equal"
        return response

    async def sign_in_new_user_by_access_token(self) -> str:
        await self.superuser_sign_in()
        fake_email = self.fake_data.email()
        fake_password = self.fake_data.password(
            length=10, special_chars=True, digits=True, upper_case=True, lower_case=True
        )
        rsp_new_user = await self.client.auth.sign_up(
            {"email": fake_email, "password": fake_password}
        )
        access_token = rsp_new_user.session.access_token
        self.client = await create_client(self.url, self.key, access_token)
        return rsp_new_user.user.id
