"""
-*- coding: utf-8 -*-
@Organization : SupaVision
@Author       : 18317
@Date Created : 06/01/2024
@Description  :
"""
import pytest
from postgrest import APIResponse

from tests.base_client import TestBaseClient


class TestPostgrestClient(TestBaseClient):
    @pytest.mark.asyncio
    async def test_insert(self):
        rsp = await self.superuser_sign_in()
        self.client.postgrest.auth(rsp.session.access_token)
        assert rsp.session.user is not None, "user is None"
        text = self.fake_data.text()
        api_rsp: APIResponse = (
            await self.client.table("test_table")
            .insert([{"user_id": rsp.session.user.id, "text": text}])
            .execute()
        )
        assert api_rsp.data[0]["user_id"] == rsp.session.user.id, "user_id is not equal"
        assert api_rsp.data[0]["text"] == text, "text is not equal"




        # FIXME: not work for rls of insert bu authed user, {'code': '42501', 'details': None, 'hint': None, 'message': 'new row violates row-level security policy for table "test_table"'}
