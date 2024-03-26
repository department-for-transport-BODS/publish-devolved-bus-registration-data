from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer
from utils.logger import log
import cognitojwt


from utils.exceptions import RegionIsNotSet, UserPoolIdIsNotSet, AppClientIdIsNotSet
from central_config import AWS_REGION, USERPOOL_ID, APP_CLIENT_ID


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
                app_client_id=self.APP_CLIENT_ID,
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


def get_current_group(claims: str = Depends(token_verifier)):
    """Get the current group from the claims.

    Args:
        claims (str, optional): _description_. Defaults to Depends(token_verifier).

    Returns:
        str: The current group, or raise an HTTPException with status code 403.
    """
    try:
        local_authority = claims.get("custom:local_authority")
        if local_authority:
            return local_authority
    except Exception as e:
        print("Exception", e)
        raise HTTPException(status_code=403, detail="Unauthorized!!")
