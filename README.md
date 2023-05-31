# cardboard.py

cardboard.py is a Python library for interacting with the cardboard API.

PyPi: https://pypi.org/project/cardboard/

## Installation

You can install the cardboard.py library using pip:

`pip install cardboard.py`

## Usage

Initialize the Cardboard or CardboardAsync class. Make sure to pass `client_secret` and `client_id`.

You can now use the client to make requests.

### Example

```python
# Python Example
```

### Async Example
```python
# Python Async Example
```

# Documentation
For detailed documentation on the Cardboard API, read https://www.guilded.gg/CardBoard/groups/3y446Rmz/channels/4539a4f9-fb51-4a23-b01-0fcaeaf062d3/docs/374610

For detailed documentation on how to use the cardboard.py library, please wait while we write it lol.

### Methods
A list of methods you can call with either Cardboard or CardboardAsync.
- `.revoke_token(token:str)` (bool)
- `.get_token(code:str)` (class AuthToken)
    - `.token` (str)
    - `.token_type` (str)
    - `.refresh_token` (str)
    - `.expires_in` (int)
    - `._raw` (dict)
- `.refresh_token(refresh_token:str)` (class AuthToken)
    - `.token` (str)
    - `.token_type` (str)
    - `.refresh_token` (str)
    - `.expires_in` (int)
    - `._raw` (dict)
- `.get_user(token:str)` (class User)
    - BEING DEVELOPED, NOTHING HERE IS DONE. WILL RAISE AN ERROR.
    - `.name` (str)
    - `.id` (str)
    - `.subdomain` (str)
    - `.aliases` (list(class UserAlias))
        - ??? (being developed)
    - ??? (being developed)

# License
This project is licensed under the MIT License. See the LICENSE file for details.
