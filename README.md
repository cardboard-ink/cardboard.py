# cardboard.py

cardboard.py is a Python library for interacting with the cardboard API.

PyPi: https://pypi.org/project/cardboard.py/

## Installation

You can install the cardboard.py library using pip:

`pip install cardboard.py`

## Usage

Initialize the Cardboard or CardboardAsync class. Make sure to pass `secret` and `client_id`.

You can now use the client to make requests.

### Examples
These examples will use Flask. Install it with `pip install Flask`

Flask is included with `cardboard.py>=0.0.8`

```python
# Python Example
from flask import Flask, request, redirect, url_for, session, Response
from cardboard import Cardboard

app = Flask(__name__)
cb = Cardboard(client_id='', secret='') # get these at https://cardboard.ink
app.secret_key = 'hi' # set this to something secure, please.

@app.route('/login')
def login():
    args = request.args
    code = args.get('code')
    if not code:
        return redirect(cb.app_url)
    try:
        token = cb.get_token(code)
    except:
        return redirect(cb.app_url)
    session['cardboard_token'] = token.token
    return redirect(url_for('dashboard'))

@app.route('/dashboard')
def dashboard():
    token = session.get('cardboard_token')
    if not token:
        return redirect(cb.app_url)
    user = cb.get_user(token)
    return Response(f'{user.name} (user id {user.id})', mimetype='text/plain')

@app.route('/')
def home():
    html = f'<html><head><title>Button Redirect</title></head><body><button onclick="window.location.href=\'{url_for("login")}\';">Login</button></body></html>'
    return Response(html, mimetype='text/html')

@app.route('/logout')
def logout():
    b = session.pop('cardboard_token', None)
    if b:
        try:
            cb.revoke_token(b)
        except:
            pass
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000)
```

```python
# Python Example using FlaskIntegration
from flask import Flask, request, redirect, url_for, session, Response
from cardboard import Cardboard, FlaskIntegration

app = Flask(__name__)
app.secret_key = 'hi' # set this to something secure, please.
cb = Cardboard(client_id='', secret='') # get these at https://cardboard.ink
cb.fi = FlaskIntegration(app=app, cardboard=cb) # make this class ONLY AFTER YOU SET A SECRET KEY for FLASK.

@app.route('/login')
@cb.fi.autologin
def login(token):
    return redirect(url_for('dashboard'))

@app.route('/dashboard')
@cb.fi.logged_in
def dashboard(token):
    user = cb.get_user(token.token)
    return Response(f'{user.name} (user id {user.id})', mimetype='text/plain')

@app.route('/')
def home():
    html = f'<html><head><title>Button Redirect</title></head><body><button onclick="window.location.href=\'{url_for("login")}\';">Login</button></body></html>'
    return Response(html, mimetype='text/html')

@app.route('/logout')
@cb.fi.autologout
def logout():
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000)
```

### Async Example
```python
# Python Async Example
```

# Documentation
For detailed documentation on the Cardboard API, read https://www.guilded.gg/CardBoard/groups/3y446Rmz/channels/4539a4f9-fb51-4a23-b014-0fcaeaf062d3/docs/374610

For detailed documentation on how to use the cardboard.py library, please wait while we write it lol.

### Methods
A list of methods/attributes you can call with either Cardboard or CardboardAsync.
- `.app_url` (str)
- `.app_name` (str)
- `.secret` (str)
- `.client_id` (str)
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
    - `.name` (str)
    - `.id` (str)
    - `.subdomain` (str)
    - `.aliases` (list(class UserAlias))
        - `.alias` (str|None)
        - `.discriminator` (str|None)
        - `.name` (str)
        - `.createdAt` (datetime)
        - `.editedAt` (datetime)
        - `._raw_createdAt` (str)
        - `._raw_editedAt` (str)
        - `.userId` (str)
        - `.gameId` (int)
        - `.socialLinkSource` (str|None)
        - `.socialLinkHandle` (str|None)
        - `.additionalInfo` (dict)
        - `.playerInfo` (dict|None)
        - `._raw` (dict)
    - `.avatar` (str)
    - `.banner` (str)
    - `.status` (class UserStatus)
        - `.text` (str|None)
        - `.reaction_id` (int|None)
        - `._raw` (dict)
        - `._raw_text` (dict)
        - `._raw_reaction` (dict)
    - `.moderationStatus` (str|None)
    - `.aboutInfo` (class userAbout)
        - `.bio` (str|None)
        - `.tagline` (str|None)
        - `._raw` (dict)
    - `.userTransientStatus` (str|None)
    - `._raw` (dict)
- `.check_token(token:str)` (bool)

### FlaskIntegration
- `@logged_in`
- `@autologin`
- `@autologout`
- `@login_autoexchange` **DEPRECATED**
- `@login_code` **DEPRECATED**

# License
This project is licensed under the MIT License. See the LICENSE file for details.
