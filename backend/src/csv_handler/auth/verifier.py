
from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer
from utils.logger import log, console
import cognitojwt
from os import getenv

REGION = getenv("REGION", "")
USERPOOL_ID = getenv("USERPOOL_ID")
APP_CLIENT_ID = getenv('APP_CLIENT_ID')

from fastapi import HTTPException
from fastapi.security import HTTPBearer
from utils.logger import console
import cognitojwt
from os import getenv
from utils.exceptions import RegionIsNotSet, UserPoolIdIsNotSet, AppClientIdIsNotSet




http_bearer = HTTPBearer()

class TokenVerifier:
    def __init__(self, token: str):
        self.token = token
        self._initialize_params
    
    def _initialize_params(self):
        self.REGION = getenv("REGION", "REGION is not set")
        self.USERPOOL_ID = getenv("USERPOOL_ID", "USERPOOL_ID is not set")
        self.APP_CLIENT_ID = getenv('APP_CLIENT_ID', "APP_CLIENT_ID is not set")
        if (self.REGION == "REGION is not set"):
            raise RegionIsNotSet
        if (self.USERPOOL_ID == "USERPOOL_ID is not set"):
            raise UserPoolIdIsNotSet
        if (self.APP_CLIENT_ID == "APP_CLIENT_ID is not set"):
            raise AppClientIdIsNotSet


    def verify_token(self):
        try:
            verified_claims: dict = cognitojwt.decode(
                self.token,
                self.REGION,
                self.APP_CLIENT_ID,
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
    print("token", token.credentials)
    verify = TokenVerifier(token.credentials).verify_token()
    print("verify", verify)
    if not verify:
        raise HTTPException(status_code=403, detail="Unauthorized")

        