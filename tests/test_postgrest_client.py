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
    async def test_create(self):
        user_id = await self.sign_in_new_user_by_access_token()
        assert self.client is not None, "client is None"
        text = self.fake_data.text()
        api_rsp: APIResponse = (
            await self.client.table("test_table")
            .insert([{"user_id": user_id, "test_data": text}])
            .execute()
        )

        assert api_rsp.data[0]["user_id"] == user_id, "user_id is not equal"
        assert api_rsp.data[0]["test_data"] == text, "text is not equal"

        # FIXME: not work for rls of insert bu authed user, {'code': '42501', 'details': None, 'hint': None, 'message': 'new row violates row-level security policy for table "test_table"'}

    @pytest.mark.asyncio
    async def test_update(self):
        user_id = await self.sign_in_new_user_by_access_token()
        assert self.client is not None, "client is None"
        text = self.fake_data.text()
        api_rsp: APIResponse = (
            await self.client.table("test_table")
            .insert([{"user_id": user_id, "test_data": text}])
            .execute()
        )

        assert api_rsp.data[0]["user_id"] == user_id, "user_id is not equal"
        assert api_rsp.data[0]["test_data"] == text, "text is not equal"

        text = self.fake_data.text()
        api_rsp: APIResponse = (
            await self.client.table("test_table")
            .update({"test_data": text})
            .eq("user_id", user_id)
            .execute()
        )
        assert api_rsp.data[0]["test_data"] == text, "text is not equal"

    @pytest.mark.asyncio
    async def test_delete(self):
        user_id = await self.sign_in_new_user_by_access_token()
        assert self.client is not None, "client is None"
        text = self.fake_data.text()
        api_rsp_1: APIResponse = (
            await self.client.table("test_table")
            .insert([{"user_id": user_id, "test_data": text}])
            .execute()
        )

        assert api_rsp_1.data[0]["user_id"] == user_id, "user_id is not equal"
        assert api_rsp_1.data[0]["test_data"] == text, "text is not equal"

        api_rsp_2: APIResponse = (
            await self.client.table("test_table")
            .delete()
            .eq("user_id", user_id)
            .execute()
        )
        assert (
            api_rsp_2.data[0]["id"] == api_rsp_1.data[0]["id"]
        ), "user_id is not equal"
        assert api_rsp_2.data[0]["test_data"] == text, "text is not equal"

    @pytest.mark.asyncio
    async def test_select(self):
        user_id = await self.sign_in_new_user_by_access_token()
        assert self.client is not None, "client is None"
        text = self.fake_data.text()
        (__, data_1), _ = (
            await self.client.table("test_table")
            .insert([{"user_id": user_id, "test_data": text}])
            .execute()
        )

        assert data_1[0]["user_id"] == user_id, "user_id is not equal"
        assert data_1[0]["test_data"] == text, "text is not equal"

        (__, data_2), _ = (
            await self.client.table("test_table")
            .select("*")
            .eq("id", data_1[0]["id"])
            .execute()
        )
        assert data_1[0]["id"] == data_2[0]["id"], "user_id is not equal"
        assert data_2[0]["test_data"] == text, "text is not equal"
