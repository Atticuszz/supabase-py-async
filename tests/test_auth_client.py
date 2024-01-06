import pytest
from dotenv import load_dotenv
from gotrue import AuthResponse, Session, UserAttributes

from tests.base_client import TestBaseClient

load_dotenv()


class TestAuth(TestBaseClient):
    @pytest.mark.asyncio
    async def test_update_user(self):
        rsp = await self.superuser_sign_in()
        assert rsp.session.user is not None, "user is None"
        name = self.fake_data.name()
        user_attr = UserAttributes(data={"name": name})
        await self.client.auth.update_user(user_attr)
        user_r = await self.client.auth.get_user()
        assert user_r.user.user_metadata["name"] == name

    @pytest.mark.asyncio
    async def test_retrieve_user(self):
        rps_super = await self.superuser_sign_in()
        assert rps_super.session.user is not None, "user is None"
        pre_user = await self.client.auth.get_user()
        rsp_user = await self.client.auth.sign_in_with_password(
            {"email": "1831768457@qq.com", "password": "Zz030327#"}
        )
        assert rsp_user.session.user is not None, "user is None"
        after_user = await self.client.auth.get_user(jwt=rsp_user.session.access_token)
        assert pre_user.user.id != after_user.user.id, "id is equal"
        assert (
            pre_user.user.email != after_user.user.email
        ), "after get_user email is  equal"

        assert (
            after_user.user.email == "1831768457@qq.com"
        ), "after get_user email is not equal"
        rps = await self.client.auth.get_session()
        assert (
            rps.user.email == "1831768457@qq.com"
        ), "after get_session email is not equal"

    @pytest.mark.asyncio
    async def test_sign_up(self):
        rsp_super = await self.superuser_sign_in()
        assert rsp_super.session.user is not None, "user is None"
        email = self.fake_data.email()
        name = self.fake_data.name()
        password = self.fake_data.password(
            length=10, special_chars=True, digits=True, upper_case=True, lower_case=True
        )
        rsp_new_user: AuthResponse = await self.client.auth.sign_up(
            {"email": email, "password": password, "options": {"data": {"name": name}}}
        )
        # sign up check
        assert rsp_new_user.user.email == email, "new user email is not equal"

        # assume activated user
        rsp_sign_user = await self.client.auth.sign_in_with_password(
            {"email": email, "password": password}
        )

        # session check
        assert (
            rsp_sign_user.session.user.user_metadata["name"] == name
        ), "user.user_metadata name is not equal"
        assert rsp_sign_user.session.user.email == email, "sign user email is not equal"
        rsp_get_user = await self.client.auth.get_user(
            jwt=rsp_sign_user.session.access_token
        )
        assert rsp_get_user.user.email == email, "get user email is not equal"

    @pytest.mark.asyncio
    async def test_get_session(self):
        rsp_super = await self.superuser_sign_in()
        assert rsp_super.session.user is not None, "user is None"
        session: Session = await self.client.auth.get_session()
        assert session.user.id == rsp_super.session.user.id, "user id is not equal"

    @pytest.mark.asyncio
    async def test_refresh_session(self):
        rsp_super = await self.superuser_sign_in()
        assert rsp_super.session.user is not None, "user is None"
        rsp: AuthResponse = await self.client.auth.refresh_session()
        assert (
            rsp.session.refresh_token != rsp_super.session.refresh_token
        ), "refresh_token is equal"
