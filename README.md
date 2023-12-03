# supabase-py-async

[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg?label=license)](https://opensource.org/licenses/MIT)
[![CI](https://github.com/Atticuszz/supabase-py-async/actions/workflows/ci.yml/badge.svg)](https://github.com/Atticuszz/supabase-py-async/actions/workflows/ci.yml)
[![Python](https://img.shields.io/pypi/pyversions/supabase-py-async)](https://pypi.org/project/supabase-py-async)
[![Version](https://img.shields.io/pypi/v/supabase-py-async?color=%2334D058)](https://pypi.org/project/supabase-py-async)

<!-- Add more badges as needed -->
[![Downloads](https://pepy.tech/badge/supabase-py-async)](https://pepy.tech/project/supabase-py-async)
[![Open Issues](https://img.shields.io/github/issues/Atticuszz/supabase-py-async)](https://github.com/Atticuszz/supabase-py-async/issues)
[![Pull Requests](https://img.shields.io/github/issues-pr/Atticuszz/supabase-py-async)](https://github.com/Atticuszz/supabase-py-async/pulls)
[![Contributors](https://img.shields.io/github/contributors/Atticuszz/supabase-py-async)](https://github.com/Atticuszz/supabase-py-async/graphs/contributors)
[![Code Size](https://img.shields.io/github/languages/code-size/Atticuszz/supabase-py-async)](https://github.com/Atticuszz/supabase-py-async)

Supabase client for Python with Async support. This project is an asynchronous variant
of [supabase-py](https://github.com/supabase-community/supabase-py) and mirrors the design
of [supabase-js](https://github.com/supabase/supabase-js/blob/master/README.md).

but i am not hahah👻,it doesn't mirrors the design of supabase-js ,py is not frontend language,we must change the design
and cater to the python web framework like fastapi,etc

# NOTE: it just the the async version of supabase-py with more code examples here ,code is almost same as supabase-py

## Status

| Status | Stability    | Goal                                                                                                              |
|--------|--------------|-------------------------------------------------------------------------------------------------------------------|
| 🚧     | Alpha        | We are testing Supabase with a closed set of customers                                                            |
| 🚧     | Public Alpha | Anyone can sign up over at [app.supabase.io](https://app.supabase.com). But go easy on us, there are a few kinks. |
| ❌      | Public Beta  | Stable enough for most non-enterprise use-cases                                                                   |
| ❌      | Public       | Production-ready                                                                                                  |

## Installation

### PyPi Installation

To install the package for Python 3.7 and above:

```bash
# with pip
pip install supabase-py-async

# with poetry
poetry add supabase-py-async
```

### Local Installation

For local development, clone this repo and install in Development mode with `pip install -e`.

## What's new?

### 2.2.0

- followed the supabase-py 2.2.0
- NOTE:!!!! we changed the way of to let the supabase_client to know who send the request by self.auth.set_session(
  access_token,refresh_token) instead of pass auth_client in to operation func like self.table('your_table').select('*')
  .execute()

### 2.1.0

- removed store client
- followed the supabase-py 2.1.0

### 2.0.5

#### new functions

- add auth_clients in AsyncClient which should be sent in operation functions like client.table,etc
- add add_auth_clients function in AsyncClient which can add auth_clients in AsyncClient as the request is sign in or
  sign up,etc
- add update_auth_session function in AsyncClient which can update auth_client by access_token from the request

#### new ideas

- and we do not need to create a new client every time we want to do a operation,so i add auth_clients in AsyncClient
  which should be sent in operation functions like client.table,etc

#### my questions

- i think we should add a new functions that can clean the auth_clients in AsyncClient schedulely,cause the auth_clients
  may be too much and it may cause some problems

## Async Usage

It's usually best practice to set your api key environment variables in some way that version control doesn't track
them, e.g don't put them in your python modules! Set the key and url for the supabase instance in the shell, or better
yet, use a dotenv file. Heres how to set the variables in the shell.

```bash
export SUPABASE_URL="my-url-to-my-awesome-supabase-instance"
export SUPABASE_KEY="my-supa-dupa-secret-supabase-api-key"
```

This client is designed to be used asynchronously. Below are some examples on how to use it.

### Initialize Supabase Client and Auth in request

```python
from fastapi import FastAPI, Depends, HTTPException, Header
from pydantic import BaseModel
from typing import Optional
from supabase import create_client, Client

app = FastAPI()

SUPABASE_URL = "your_supabase_url"
SUPABASE_KEY = "your_supabase_anon_key"

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)


class UserLogin(BaseModel):
  email: str
  password: str


@app.post("/login")
async def login(user: UserLogin):
  response = await supabase.auth.sign_in_with_password(
    email=user.email, password=user.password
  )
  if response.error:
    raise HTTPException(status_code=400, detail=response.error.message)
  return response.session


async def get_current_user(authorization: Optional[str] = Header(None)):
  if not authorization:
    raise HTTPException(status_code=401, detail="Unauthorized")
  tokens = authorization.split(" ")

  # Check if there are two tokens (access token and refresh token)
  if len(tokens) != 2:
    raise HTTPException(status_code=401, detail="Invalid authorization header format")

  # Extract the access token and refresh token
  access_token, refresh_token = tokens
  try:
    session = await supabase.auth.set_session(access_token=access_token, refresh_token=refresh_token)
    return session
  except Exception as e:
    raise HTTPException(status_code=401, detail="Invalid token")


@app.get("/protected")
async def protected_route(session: dict = Depends(get_current_user)):
  result = await supabase.table('your_table').select('*').execute()
  return result.data


@app.post("/refresh-token")
async def refresh_token(refresh_token: str):
  try:
    new_session = await supabase.auth.refresh_session(refresh_token)
    return new_session
  except Exception as e:
    raise HTTPException(status_code=401, detail="Could not refresh token")

```

### Async Data Operations

```python
async def data_operations():
  auth_response: AuthResponse = await self.auth.sign_in_with_password({"email": ur_email, "password": ur_password)
  #  or other sign in methods    
  # Insert
  insert_data = await supabase.table("countries").insert({"name": "Germany"}).execute()

  # Select
  select_data = await supabase.table("countries").select("*").eq("country", "IL").execute()

  # Update
  update_data = await supabase.table("countries").update(
    {"country": "Indonesia", "capital_city": "Jakarta"}).eq("id", 1).execute()

  # Delete
  delete_data = await supabase.table("countries").delete().eq("id", 1).execute()

  # note: if you wanna handle the different users,you should called  self.auth.set_session(access_token,refresh_token)
  #  and then you can use the auth_clients in AsyncClient in the request that set_session is called
  asyncio.run(data_operations())
```

<!-- Include more examples and documentation links -->

See [Supabase Docs](https://supabase.com/docs/guides/client-libraries) for a full list of examples.

## Contributions
Welcome to the supabase-py-async package! 😊

Hello, fellow developers!

I'm excited to share that I've published an **asynchronous package for Supabase** designed to work smoothly with FastAPI, and it's now open for contributions! 🚀

This project is very close to my heart ❤️, cause my personal plan app is based on vue and fastapi so i need a async one，and hope it will benefit yours as well，and I believe that with your valuable contributions, we can make it even better. Whether it's improving the code, fixing bugs, writing documentation, or suggesting new features – all contributions are welcome.

If you're passionate about FastAPI, async programming in Python, or just want to lend a hand with a growing project, this is your invitation to join in. Let's collaborate to create something amazing that we're all proud of. 🤝

### How to Contribute
- **Fork the repository:** Start by forking the project to your GitHub account.
- **Pick an issue:** Look for open issues that interest you or suggest new ones.
- **Open a pull request:** After making your changes, open a pull request with a clear description of your improvements

### Stay Connected
- **Join our community chat:** We have a Discord channel (https://discord.com/invite/QPysZkKT) where we discuss the project and collaborate.
- **Stay updated:** Watch this repository to stay informed about new issues and updates.

Contributing to open source is a rewarding way to learn, teach, and build experience. No matter your skill level, your contributions are invaluable to the project. 🌟

Thank you for considering contributing to this project. Let's make it the best it can be, together!

Happy coding! 👨‍💻👩‍💻

Atticus Zhou
