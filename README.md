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

### Initialize Supabase Client

```python
import os
from supabase_py_async import create_client, AsyncClient

url: str = os.environ.get("SUPABASE_URL")

key: str = os.environ.get("SUPABASE_KEY")

supabase: AsyncClient = create_client(url, key)
```

### Async Data Operations

```python
async def data_operations():
    # Note:  opereations should be sent operator(auth_client)!!
    auth_response: AuthResponse = await self.auth.sign_in_with_password({"email": ur_email, "password": ur_password)
    #  or other sign in methods
    await supabase.add_auth_clients(auth_response)
    # next time your can use operation with supabase like this,i assume you get a user access_token
    auth_client = await self.update_auth_session(auth_response.seesion.access_token)  # or access_token from other place

    # Insert
    insert_data = await supabase.table("countries", auth_client).insert({"name": "Germany"}).execute()

    # Select
    select_data = await supabase.table("countries", auth_client).select("*").eq("country", "IL").execute()

    # Update
    update_data = await supabase.table("countries", auth_client).update(
        {"country": "Indonesia", "capital_city": "Jakarta"}).eq("id", 1).execute()

    # Delete
    delete_data = await supabase.table("countries", auth_client).delete().eq("id", 1).execute()

    # note: every operation should be get a auth_client from access_token
    asyncio.run(data_operations())
```

### Async Authentication

```python
async def async_auth():
  random_email: str = "email@example.com"
  random_password: str = "supersecurepassword"
  auth_response: AuthResponse = await supabase.auth.sign_up(email=random_email, password=random_password)


asyncio.run(async_auth())
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
