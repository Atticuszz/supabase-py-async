# coding=utf-8
import os

import pytest
from dotenv import load_dotenv
from gotrue import AuthResponse, UserResponse, Session

from supabase_py_async import create_client

load_dotenv()


@pytest.mark.asyncio
async def test_get_all():
    # 获取test.env中的环境变量
    url = os.getenv("SUPABASE_TEST_URL")
    key = os.getenv("SUPABASE_TEST_KEY")
    # 创建客户端
    client = await create_client(url, key)
    response = await client.table("task_done_list").select("*").execute()
    print(response.data)


@pytest.mark.asyncio
async def test_sign_in():
    # 获取test.env中的环境变量
    url = os.getenv("SUPABASE_TEST_URL")
    key = os.getenv("SUPABASE_TEST_KEY")
    # 创建客户端
    client = await create_client(url, key)
    response: AuthResponse = await client.auth.sign_in_with_password(
        {'email': 'zhouge1831@gmail.com', 'password': 'Zz030327#'}
    )

    print(response)


@pytest.mark.asyncio
async def test_operate_with_token():
    # 获取test.env中的环境变量
    url = os.getenv("SUPABASE_TEST_URL")
    key = os.getenv("SUPABASE_TEST_KEY")
    # 创建客户端
    client = await create_client(url, key)
    response_1: AuthResponse = await client.auth.sign_in_with_password(
        {'email': 'zhouge1831@gmail.com', 'password': 'Zz030327#'}
    )

    # print(response)
    user_r: UserResponse = await client.auth.get_user()
    print("before sign in with user_1,called get_user", user_r.user.email)

    response_2: AuthResponse = await client.auth.sign_in_with_password(
        {'email': '1831768457@qq.com', 'password': 'Zz030327#'}
    )
    user_r_2: UserResponse = await client.auth.get_user()
    print("after sign in with user_2,called get_user", user_r_2.user.email)

    response_3: AuthResponse = await client.auth.set_session(response_2.session.access_token,
                                                             response_2.session.refresh_token)
    print("after set_session with user_2,response_3.user", response_3.user.email)
    get_session_user_2: Session = await client.auth.get_session()
    print("after set_session with user_2,called get_session user2", get_session_user_2.user.email)
    print("after set_session with user_2,called set_session user2", await client.auth.get_user())

    response_4: AuthResponse = await client.auth.set_session(response_1.session.access_token,
                                                             response_1.session.refresh_token)
    print("after set_session with user_1,response_5.user", response_4.user.email)
    print("after set_session with user_1,called set_session user1", await client.auth.get_user())


if __name__ == '__main__':
    # asyncio.run(test_sign_in())
    #     # asyncio.run(sign_in())
    # asyncio.run(test_operate_with_token())
    pass
