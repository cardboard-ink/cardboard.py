from flask import request, Flask, redirect, session
from functools import wraps
from cardboard import Cardboard, CardboardAsync
from cardboard import Exceptions as CBE
import aiohttp, asyncio
import concurrent.futures

class FlaskIntegration:
    """
    A flask integration for Cardboard.

    Args:
        app: Your Flask app.
        cardboard: Your Cardboard app.
    """
    def __init__(self, app:Flask, cardboard:Cardboard|CardboardAsync):
        self.app:Flask = app
        self.cb:Cardboard|CardboardAsync = cardboard
        self.secret = self.cb.secret
        self.client_id = self.cb.client_id
        self.cb = CardboardAsync(client_id=self.client_id, secret=self.secret)
        self.cbsync = result = concurrent.futures.ThreadPoolExecutor().submit(lambda: Cardboard(client_id=self.client_id, secret=self.secret)).result()

        if not app.secret_key:
            raise ValueError("Flask app secret key is not set or is empty.")

    def getloop(self):
        try:
            loop = asyncio.get_event_loop()
        except RuntimeError:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
        return loop

    async def asyncpost(self, url, data=None, headers=None) -> dict|int:
        """
        Makes a post request. Returns json or int.
        """
        async with aiohttp.ClientSession() as cs:
            async with cs.post(url, data=data, headers=headers) as response:
                return await response.json() if response.status == 200 else response.status
    
    def autologin(self, route_function):
        """
        Automatically logs you in with a token, or else redirects you to the app login page. This is async.

        Returns an AuthToken class. You can get the token with token.token
        
        Usage:
            @app.route('/login')
            @fi.autologin
            def login(token:AuthToken):
                # run code, with token always valid.
        """
        @wraps(route_function)
        def decorator(*args, **kwargs):
            code = request.args.get('code')
            if code:
                grant_type = "authorization_code"
                data = {
                    "code": code,
                    "client_id": self.client_id,
                    "client_secret": self.secret,
                    "grant_type": grant_type,
                }
                loop = self.getloop()
                response = loop.run_until_complete(self.asyncpost(f"{self.cb._baseurl}/token", data=data, headers={"Content-Type": "application/x-www-form-urlencoded"}))
                if type(response) == int:
                    return redirect(self.cb.app_url)
                token = self.cb.AuthToken(response)
            else:
                return redirect(self.cb.app_url)
            return route_function(token, *args, **kwargs)
        return decorator

    def login_code(self, route_function):
        """
        Automatically passes the "code" variable instead of using request.args.get('code').

        Usage:
            @app.route('/login')
            @fi.login_code
            def login(code:str|None, *args, **kwargs):
                # your login function.
        """
        @wraps(route_function)
        def decorator(*args, **kwargs):
            code = request.args.get('code')
            return route_function(code, *args, **kwargs)
        return decorator
    
    def login_autoexchange(self, route_function):
        """
        Automatically exchanges the initial code. This is async.

        Returns None if invalid initial code.

        Usage:
            fi = FlaskIntegration(app)

            @app.route('/login')
            @fi.login_autoexchange
            def login(token:AuthToken|None, *args, **kwargs):
                # your login function.
        """
        @wraps(route_function)
        def decorator(*args, **kwargs):
            code = request.args.get('code')
            if code:
                grant_type = "authorization_code"
                data = {
                    "code": code,
                    "client_id": self.client_id,
                    "client_secret": self.secret,
                    "grant_type": grant_type,
                }
                loop = self.getloop()
                response = loop.run_until_complete(self.asyncpost(f"{self.cb._baseurl}/token", data=data, headers={"Content-Type": "application/x-www-form-urlencoded"}))
                if type(response) == int:
                    token = None
                else:
                    token = self.cb.AuthToken(response)
            else:
                token = None
            return route_function(token, *args, **kwargs)
        return decorator
    
    def logged_in(self, name, check=False):
        """
        Checks if the user is logged in with a valid auth token. Redirects to the app login if not valid. Checking is done in a seperate thread.
        
        Args:
            name (str): The name used in the Flask session.
            check (bool=False): Whether or not to check if the token is valid. You can choose to do this in the function yourself.
        """
        def decorator(route_function):
            @wraps(route_function)
            def wrapper(*args, **kwargs):
                if name in session:
                    token:str = session.get(name)
                    if check:
                        # response = self.cbsync.check_token(token)
                        response = concurrent.futures.ThreadPoolExecutor().submit(lambda: self.cbsync.check_token(token)).result()
                        if not response:
                            return redirect(self.cb.app_url)
                    return route_function(token, *args, **kwargs)
                else:
                    return redirect(self.cb.app_url)
            return wrapper
        return decorator