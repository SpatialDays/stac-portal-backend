import jwt
from .aadtoken import get_public_key
from flask import current_app
from functools import wraps
from inspect import getfullargspec
from flask import request, abort
from typing import Any, Callable, Dict, List
from dotenv import load_dotenv
import logging

load_dotenv()


class AuthDecorator:
    def __init__(self):
        pass

    def auth_token(self, token: str) -> dict:
        """
        Validates a JWT token and returns the payload
        """
        try:
            public_key = get_public_key(token)
            decoded = jwt.api_jwt.decode_complete(
                token,
                public_key,
                verify=True,
                algorithms=["RS256"],
                audience=[self.client_id],
                issuer=self.issuer,
                # options={
                #     "verify_iat": False,
                #     "verify_exp": False,
                #     "verify_signature": True,
                # }
            )
            return decoded["payload"]
        except Exception as e:
            raise Exception(f"Error decoding token: {e}")

    def header_decorator(self, allowed_roles: List[str] = []):
        def decorator_function(f: Callable[..., Any]):
            # Get function arguments
            func_args = getfullargspec(f).args

            @wraps(f)
            def decorated_function(*args, **kwargs):
                # Extract the Authorization header value
                self.client_id = current_app.config["AD_CLIENT_ID"]
                self.tenant_id = current_app.config["AD_TENANT_ID"]
                self.issuer = f"https://login.microsoftonline.com/{self.tenant_id}/v2.0"
                header_value = request.headers.get("Authorization")

                if header_value:
                    # Extract the token from the header value
                    token = header_value[7:]
                    # Decode the token using auth_decorator.auth_token(token)
                    try:
                        decoded_token: Dict[str, Any] = self.auth_token(token)
                    except Exception as e:
                        # Return a 401 Unauthorized response
                        logging.info(f"Error decoding token: {e}")
                        abort(401,f"Error decoding token: {e}")

                    # Extract the roles from the decoded token
                    roles = decoded_token["roles"]

                    # Check if the user's role is allowed
                    # could we do:
                    # authenticated = any(role in allowed_roles for role in roles)
                    authenticated = False
                    for i in roles:
                        for j in allowed_roles:
                            if i == j:
                                authenticated = True
                                break

                    if not authenticated:
                        # Return a 401 Unauthorized response
                        abort(401,f"Role not allowed")

                    # Update kwargs with values from decoded_token
                    for arg_name in func_args:
                        if arg_name in decoded_token:
                            kwargs[arg_name] = decoded_token[arg_name]

                    # Call the original function with its arguments
                    return f(*args, **kwargs)
                else:
                    # Return a 401 Unauthorized response
                    abort(401,"No Authorization header provided")

            return decorated_function

        return decorator_function