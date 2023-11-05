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
  # Insert
  insert_data = await supabase.table("countries").insert({"name": "Germany"}).execute()

  # Select
  select_data = await supabase.table("countries").select("*").eq("country", "IL").execute()

  # Update
  update_data = await supabase.table("countries").update({"country": "Indonesia", "capital_city": "Jakarta"}).eq("id",
                                                                                                                 1).execute()

  # Delete
  delete_data = await supabase.table("countries").delete().eq("id", 1).execute()


asyncio.run(data_operations())
```

### Async Authentication

```python
async def async_auth():
  random_email: str = "email@example.com"
  random_password: str = "supersecurepassword"
  user = await supabase.auth.sign_up(email=random_email, password=random_password)


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
