from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer
from utils.logger import console, log
import cognitojwt


from utils.exceptions import RegionIsNotSet, UserPoolIdIsNotSet, AppClientIdIsNotSet
from central_config import PROJECT_ENV, AWS_REGION, USERPOOL_ID, APP_CLIENT_ID


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
            verified_claims: dict = cognitojwt.decode(
                self.token,
                self.REGION,
                self.USERPOOL_ID,
                app_client_id=self.APP_CLIENT_ID,
            )
            console.log(verified_claims)
            return True
        except cognitojwt.CognitoJWTException as e:
            console.log(e)
            return False
        except Exception as e:
            console.print_exception()
            console.log(e)
            return False


def token_verifier(token: str = Depends(http_bearer)):
    """ Verify the token using the TokenVerifier class.

    Args:
        token (str, optional): The token to be verified. Defaults to Depends(http_bearer).

    Raises:
        HTTPException: If the token is invalid, raise an HTTPException with status code 403.
    """
    # Verify if its in localdev and token is localdev
    if PROJECT_ENV == "localdev" and token.credentials == "localdev":
        return
    verify = TokenVerifier(token.credentials).verify_token()
    log.debug(f"Token verification status: {verify}")
    if not verify:
        raise HTTPException(status_code=403, detail="Unauthorized")
