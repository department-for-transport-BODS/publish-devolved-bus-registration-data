from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer
from utils.logger import log
import cognitojwt

from utils.pydant_model import AuthenticatedEntity
from utils.exceptions import RegionIsNotSet, UserPoolIdIsNotSet, AppClientIdIsNotSet
from central_config import AWS_REGION, USERPOOL_ID, APP_CLIENT_ID
from typing import Tuple


http_bearer = HTTPBearer()


class TokenVerifier:
    """
    Class to verify tokens using Cognito JWT library.
    """

    def __init__(self, token: str):
        """
        Initialize the TokenVerifier object.

        Args:
            token (str): The token to be verified.
        """
        self.token = token
        self._initialize_params()

    def _initialize_params(self):
        """
        Initialize the required parameters for token verification.
        Raises exceptions if any of the parameters are not set.
        """
        self.REGION = AWS_REGION
        self.USERPOOL_ID = USERPOOL_ID
        self.APP_CLIENT_ID = APP_CLIENT_ID
        if self.REGION == "REGION is not set":
            raise RegionIsNotSet
        if self.USERPOOL_ID == "USERPOOL_ID is not set":
            raise UserPoolIdIsNotSet
        if self.APP_CLIENT_ID == "APP_CLIENT_ID is not set":
            raise AppClientIdIsNotSet

    def verify_token(self):
        """
        Verify the token using Cognito JWT library.

        Returns:
            bool: True if the token is valid, False otherwise.
        """
        try:
            self.claims = None
            self.claims: dict = cognitojwt.decode(
                self.token,
                self.REGION,
                self.USERPOOL_ID,
                # app_client_id=self.APP_CLIENT_ID,
            )
            return True
        except Exception:
            return False


def token_verifier(token: str = Depends(http_bearer)):
    """Verify the token using the TokenVerifier class.

    Args:
        token (str, optional): The token to be verified. Defaults to Depends(http_bearer).

    Raises:
        HTTPException: If the token is invalid, raise an HTTPException with status code 403.
    """
    # Verify if its in local and token is local
    verification = TokenVerifier(token.credentials)
    verify = verification.verify_token()
    if verify:
        return verification.claims
    log.debug(f"Token verification status: {verify}")
    if not verify:
        raise HTTPException(status_code=403, detail="Unauthorized")


def is_an_app(claims: dict) -> Tuple[bool, str]:
    scope = claims.get("scope")
    if scope:
        app_name = scope.split("/")[-1]
        if len(app_name) > 0:
            return True, app_name
    return False, None

def is_a_local_authority(claims: dict) -> Tuple[bool, str]:
    username = claims.get("custom:local_authority")
    if username:
        return True, username
    return False, None


def get_local_authority(claims: dict = Depends(token_verifier)):
    return get_entity(claims, only_local_authority=True)




def get_entity(claims: dict = Depends(token_verifier),only_local_authority=Depends((lambda: False)))-> AuthenticatedEntity|HTTPException:
    """Check the identity weather its a local authority or an app.

    Args:
        claims (dict, optional): _description_. Defaults to Depends(token_verifier).

    Returns:
        AuthenticatedEntity: The current user/app, or raise an HTTPException with status code 403.
    """
    
    is_local_authority, username = is_a_local_authority(claims)
    if is_local_authority and len(username) > 0:
        return AuthenticatedEntity(type="local_auth", name=username)
    
    if not only_local_authority:
        is_app, app_name = is_an_app(claims)
        if  is_app and len(app_name) > 0:
            return AuthenticatedEntity(type="app", name=app_name)

    raise HTTPException(status_code=403, detail="Unauthorized!!")
