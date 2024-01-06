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

async-part of supabase-py Python client for [Supabase](https://supabase.com)

- Documentation: [supabase.com/docs](https://supabase.com/docs/reference/python/introduction)
- Usage:
  - [Supabase with Python fastapi app](https://github.com/Atticuszz/fastapi_supabase_template)
  - [GitHub OAuth in your Python Flask app](https://supabase.com/blog/oauth2-login-python-flask-apps)
  - [Python data loading with Supabase](https://supabase.com/blog/loading-data-supabase-python)


## Installation

We recommend activating your virtual environment. For example, we like `poetry` and `conda`!

### PyPi installation

Install the package (for > Python 3.7):

```bash
# with pip
pip install supabase-py-async
# with poetry (recommended)
poetry add supabase-py-async
```

### Local installation

You can also install locally after cloning this repo. Install Development mode with ``pip install -e``, which makes it so when you edit the source code the changes will be reflected in your python module.

## Usage

Set your Supabase environment variables in a dotenv file, or using the shell:

```bash
export SUPABASE_URL="my-url-to-my-awesome-supabase-instance"
export SUPABASE_KEY="my-supa-dupa-secret-supabase-api-key"
```

We can then read the keys in the python source code:

```python
import os
from supabase_py_async import create_client, AsyncClient

url: str = os.environ.get("SUPABASE_URL")
key: str = os.environ.get("SUPABASE_KEY")
supabase: Client = create_client(url, key)
```

Use the supabase client to interface with your database.

#### Authenticate

```python
from supabase import create_client, Client

url: str = os.environ.get("SUPABASE_TEST_URL")
key: str = os.environ.get("SUPABASE_TEST_KEY")
supabase: Client = create_client(url, key)
# Create a random user login email and password.
random_email: str = "3hf82fijf92@supamail.com"
random_password: str = "fqj13bnf2hiu23h"
user = supabase.auth.sign_up({ "email": random_email, "password": random_password })
```

#### Sign-in

```python
from supabase import create_client, Client

url: str = os.environ.get("SUPABASE_TEST_URL")
key: str = os.environ.get("SUPABASE_TEST_KEY")
supabase: Client = create_client(url, key)
# Sign in using the user email and password.
random_email: str = "3hf82fijf92@supamail.com"
random_password: str = "fqj13bnf2hiu23h"
user = supabase.auth.sign_in_with_password({ "email": random_email, "password": random_password })
```

#### Insert Data

```python
from supabase import create_client, Client

url: str = os.environ.get("SUPABASE_TEST_URL")
key: str = os.environ.get("SUPABASE_TEST_KEY")
supabase: Client = create_client(url, key)
data = supabase.table("countries").insert({"name":"Germany"}).execute()
assert len(data.data) > 0
```

#### Select Data

```python
from supabase import create_client, Client

url: str = os.environ.get("SUPABASE_TEST_URL")
key: str = os.environ.get("SUPABASE_TEST_KEY")
supabase: Client = create_client(url, key)
data = supabase.table("countries").select("*").eq("country", "IL").execute()
# Assert we pulled real data.
assert len(data.data) > 0
```

#### Update Data

```python
from supabase import create_client, Client

url: str = os.environ.get("SUPABASE_TEST_URL")
key: str = os.environ.get("SUPABASE_TEST_KEY")
supabase: Client = create_client(url, key)
data = supabase.table("countries").update({"country": "Indonesia", "capital_city": "Jakarta"}).eq("id", 1).execute()
```

#### Update data with duplicate keys

```python
from supabase import create_client, Client

url: str = os.environ.get("SUPABASE_TEST_URL")
key: str = os.environ.get("SUPABASE_TEST_KEY")
supabase: Client = create_client(url, key)

country = {
  "country": "United Kingdom",
  "capital_city": "London" # this was missing when it was added
}

data = supabase.table("countries").upsert(country).execute()
assert len(data.data) > 0
```

#### Delete Data

```python
from supabase import create_client, Client

url: str = os.environ.get("SUPABASE_TEST_URL")
key: str = os.environ.get("SUPABASE_TEST_KEY")
supabase: Client = create_client(url, key)
data = supabase.table("countries").delete().eq("id", 1).execute()
```

#### Call Edge Functions

```python
from supabase import create_client, Client

url: str = os.environ.get("SUPABASE_TEST_URL")
key: str = os.environ.get("SUPABASE_TEST_KEY")
supabase: Client = create_client(url, key)

def test_func():
  try:
    resp = supabase.functions.invoke("hello-world", invoke_options={'body':{}})
    return resp
  except (FunctionsRelayError, FunctionsHttpError) as exception:
    err = exception.to_dict()
    print(err.get("message"))
```

#### Download a file from Storage

```python
from supabase import create_client, Client

url: str = os.environ.get("SUPABASE_TEST_URL")
key: str = os.environ.get("SUPABASE_TEST_KEY")
supabase: Client = create_client(url, key)

bucket_name: str = "photos"

data = supabase.storage.from_(bucket_name).download("photo1.png")
```

#### Upload a file

```python
from supabase import create_client, Client

url: str = os.environ.get("SUPABASE_TEST_URL")
key: str = os.environ.get("SUPABASE_TEST_KEY")
supabase: Client = create_client(url, key)

bucket_name: str = "photos"
new_file = getUserFile()

data = supabase.storage.from_(bucket_name).upload("/user1/profile.png", new_file)
```

#### Remove a file

```python
from supabase import create_client, Client

url: str = os.environ.get("SUPABASE_TEST_URL")
key: str = os.environ.get("SUPABASE_TEST_KEY")
supabase: Client = create_client(url, key)

bucket_name: str = "photos"

data = supabase.storage.from_(bucket_name).remove(["old_photo.png", "image5.jpg"])
```

#### List all files

```python
from supabase import create_client, Client

url: str = os.environ.get("SUPABASE_TEST_URL")
key: str = os.environ.get("SUPABASE_TEST_KEY")
supabase: Client = create_client(url, key)

bucket_name: str = "charts"

data = supabase.storage.from_(bucket_name).list()
```

#### Move and rename files

```python
from supabase import create_client, Client

url: str = os.environ.get("SUPABASE_TEST_URL")
key: str = os.environ.get("SUPABASE_TEST_KEY")
supabase: Client = create_client(url, key)

bucket_name: str = "charts"
old_file_path: str = "generic/graph1.png"
new_file_path: str = "important/revenue.png"

data = supabase.storage.from_(bucket_name).move(old_file_path, new_file_path)
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

### Running Tests

Currently the test suites are in a state of flux. We are expanding our clients tests to ensure things are working, and for now can connect to this test instance, that is populated with the following table:

<p align="center">
  <img width="720" height="481" src="https://i.ibb.co/Bq7Kdty/db.png">
</p>

The above test database is a blank supabase instance that has populated the `countries` table with the built in countries script that can be found in the supabase UI. You can launch the test scripts and point to the above test database by running




