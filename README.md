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

async-part of supabase-py Python client for [Supabase-py](https://github.com/supabase-community/supabase-py)

- Documentation: [supabase.com/docs](https://supabase.com/docs/reference/python/introduction)
- Usage:
  - [Supabase with Python ⚡fastapi⚡ app](https://github.com/Atticuszz/fastapi_supabase_template)
  - [GitHub OAuth in your Python Flask app](https://supabase.com/blog/oauth2-login-python-flask-apps)
  - [Python data loading with Supabase](https://supabase.com/blog/loading-data-supabase-python)


## Installation

We recommend activating your virtual environment. For example, we like `poetry` and `conda`!

### PyPi installation

Install the package (for > Python 3.10):

```bash
# with pip
pip install supabase-py-async
# with poetry (recommended)
poetry add supabase-py-async
```

### Local installation

You can also install locally after cloning this repo. Install Development mode with ``pip install -e``, which makes it so when you edit the source code the changes will be reflected in your python module.

## differences
what's different from [supabase-py](https://github.com/supabase-community/supabase-py)?
1. a optional of `access_token: str | None = None,` key word argument in `create_client` function, which is used to set the `Authorization` header in the request.
2. more [tests](./tests) on crud operations and auth operations.

more tutorials in
- [Supabase with Python ⚡fastapi⚡ app](https://github.com/Atticuszz/fastapi_supabase_template)

## Usage
Set your Supabase environment variables in a dotenv file, or using the shell:

```bash
export SUPABASE_URL="my-url-to-my-awesome-supabase-instance"
export SUPABASE_KEY="my-supa-dupa-secret-supabase-api-key"
```

init the client in fastapi lifespan event

```python
import os
from contextlib import asynccontextmanager
from dotenv import load_dotenv
from fastapi import FastAPI
from supabase_py_async import create_client
from supabase_py_async.lib.client_options import ClientOptions
client = None
@asynccontextmanager
async def lifespan(app: FastAPI):
    """ life span events"""
    identify_worker = None
    try:
        # start client
        load_dotenv()
        url: str = os.getenv("SUPABASE_URL")
        key: str = os.getenv("SUPABASE_KEY")
        client = await create_client(url, key, options=ClientOptions(
            postgrest_client_timeout=10, storage_client_timeout=10))
        yield
    finally:
        pass
```

Use the supabase client to interface with your database.

#### Authenticate

```python
async def authenticate(email: str, password: str):
    """ authenticate user """
     # Create a random user login email and password.
    random_email: str = "3hf82fijf92@supamail.com"
    random_password: str = "fqj13bnf2hiu23h"
    user = await client.auth.sign_in(email=email, password=password)
```

#### Sign-in

```python
async def sign_in(email: str, password: str):
    """ sign in user """
    # Sign in using the user email and password.
    random_email: str = "3hf82fijf92@supamail.com"
    random_password: str = "fqj13bnf2hiu23h"
    user =  await client.auth.sign_in_with_password({ "email": random_email, "password": random_password })
```

#### Insert Data

```python
async def insert_data():
    """ insert data """
    # Insert a new country into the 'countries' table.
    data = await client.table("countries").insert({"name":"Germany"}).execute()
    assert len(data.data) > 0
```

#### Select Data

```python
async def select_data():
    """ select data """
    # Select all countries from the 'countries' table.
    data = await client.table("countries").select("*").execute()
    assert len(data.data) > 0
```

#### Update Data

```python
async def update_data():
    """ update data """
    # Update the country with id of 1.
    data = await client.table("countries").update({"country": "Indonesia", "capital_city": "Jakarta"}).eq("id", 1).execute()
    assert len(data.data) > 0
```


#### Update data with duplicate keys

```python
async def update_data_with_duplicate_keys():
    """ update data with duplicate keys """
    # Update the country with id of 1.
    data = await client.table("countries").update({"country": "Indonesia", "capital_city": "Jakarta"}).eq("id", 1).execute()
```

#### Delete Data

```python
async def delete_data():
    """ delete data """
    # Delete the country with id of 1.
    data = await client.table("countries").delete().eq("id", 1).execute()
```


#### Call Edge Functions

```python


async def test_func():
  try:
    resp = await client.functions.invoke("hello-world", invoke_options={'body':{}})
    return resp
  except (FunctionsRelayError, FunctionsHttpError) as exception:
    err = exception.to_dict()
    print(err.get("message"))
```

#### Download a file from Storage

```python

async def download_file():
    """ download file """
    # Download a file from Storage.
    bucket_name: str = "photos"
    data = await client.storage.from_(bucket_name).download("photo1.png")
```

#### Upload a file

```python
async def upload_file():
    """ upload file """
    # Upload a file to Storage.
    bucket_name: str = "photos"
    new_file = getUserFile()
    data = await client.storage.from_(bucket_name).upload("/user1/profile.png", new_file)
```


#### Remove a file

```python
async def remove_file():
    """ remove file """
    # Remove a file from Storage.
    bucket_name: str = "photos"
    data = await client.storage.from_(bucket_name).remove(["old_photo.png", "image5.jpg"])
```


#### List all files

```python
async def list_files():
    """ list files """
    # List all files in Storage.
    bucket_name: str = "photos"
    data = await client.storage.from_(bucket_name).list()
```


#### Move and rename files

```python
async def move_files():
    """ move files """
    # Move and rename files in Storage.
    
    bucket_name: str = "charts"
    old_file_path: str = "generic/graph1.png"
    new_file_path: str = "important/revenue.png"
    
    data = await client.storage.from_(bucket_name).move(old_file_path, new_file_path)
```

## Roadmap

- [x] Wrap [Postgrest-py](https://github.com/supabase-community/postgrest-py/)
  - [ ] Add remaining filters
  - [ ] Add support for EXPLAIN
  - [ ] Add proper error handling
- [ ] Wrap [Realtime-py](https://github.com/supabase-community/realtime-py)
    - [ ]  Integrate with Supabase-py
    - [ ]  Support WALRUS
    - [ ]  Support broadcast (to check if already supported)
- [x] Wrap [auth-py](https://github.com/supabase-community/auth-py)
    - [x] Remove references to GoTrue-js v1 and do a proper release
    - [ ] Test and document common flows (e.g. sign in with OAuth, sign in with OTP)
    - [ ] Add MFA methods and SSO methods
    - [x] Add Proof Key for Code Exchange (PKCE) methods. Unlike the JS library, we do not currently plan to support Magic Link (PKCE). Please use the [token hash](https://supabase.com/docs/guides/auth/server-side/email-based-auth-with-pkce-flow-for-ssr#create-api-endpoint-for-handling-tokenhash) in tandem with `verifyOTP` instead.
- [x] Wrap [storage-py](https://github.com/supabase-community/storage-py)
    - [ ]  Support resumable uploads
    - [x]  Setup testing environment
    - [x]  Document how to properly upload different file types (e.g. jpeg/png and download it)
- [x] Wrap [functions-py](https://github.com/supabase-community/functions-py)

Overall Tasks:
- [x] Add async support across the entire library
- [ ] Add FastAPI helper library (external to supabase-py)
- [ ] Add `django-supabase-postgrest` (external to supabase-py)

## Contributing

Contributing to the Python libraries are a great way to get involved with the Supabase community. Reach out to us on Discord if you want to get involved.





