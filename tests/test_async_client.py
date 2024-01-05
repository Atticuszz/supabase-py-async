# coding=utf-8
import asyncio
import os

import faker
import pytest
from dotenv import load_dotenv
from faker import Faker
from gotrue import AuthResponse, UserResponse, Session, UserAttributes

from supabase_py_async import create_client, AsyncClient

load_dotenv()



class TestClient:
    url: str = os.getenv("SUPABASE_TEST_URL")
    key: str = os.getenv("SUPABASE_TEST_KEY")
    client: AsyncClient = None

    async def _superuser_sign_in(self):
        self.client = await create_client(self.url, self.key)
        response = await self.client.auth.sign_in_with_password(
            {'email': 'zhouge1831@gmail.com', 'password': 'Zz030327#'}
        )
        return response

    @pytest.mark.asyncio
    async def test_update_user(self):
        rsp = await self._superuser_sign_in()
        assert rsp.session.user is not None, "user is None"
        name = Faker().name()
        user_attr = UserAttributes(data={"name": name})
        await self.client.auth.update_user(user_attr)
        user_r = await self.client.auth.get_user()
        assert user_r.user.user_metadata["name"] == name

    @pytest.mark.asyncio
    async def test_new_user(self):
        rps_super = await self._superuser_sign_in()
        assert rps_super.session.user is not None, "user is None"
        pre_user = await self.client.auth.get_user()
        rsp_user = await self.client.auth.sign_in_with_password(
            {'email': '1831768457@qq.com', 'password': 'Zz030327#'}
        )
        assert rsp_user.session.user is not None, "user is None"
        after_user = await self.client.auth.get_user(jwt=rsp_user.session.access_token)
        assert pre_user.user.id != after_user.user.id, "id is equal"
        assert pre_user.user.email != after_user.user.email, "after get_user email is  equal"

        assert after_user.user.email == "1831768457@qq.com", "after get_user email is not equal"
        rps = await self.client.auth.get_session()
        assert rps.user.email == "1831768457@qq.com", "after get_session email is not equal"

    @pytest.mark.asyncio
    async def test_new_user_db_rls_curd(self):
        rsp_super = await self._superuser_sign_in()
        assert rsp_super.session.user is not None, "user is None"
        rsp_user = await self.client.auth.sign_in_with_password(
            {'email': '1831768457@qq.com', 'password': 'Zz030327#'}
        )
        assert rsp_user.session.user is not None, "user is None"
        # self.client.postgrest.auth(token=rsp_user.session.access_token)
        rsp_set_session: AuthResponse = await self.client.auth.get_user(jwt=rsp_user.session.access_token)
        # TODO: add rls test


if __name__ == '__main__':
    # asyncio.run(test_sign_in())
    #     # asyncio.run(sign_in())
    pass
