import cognitojwt

from central_config import AWS_REGION, USERPOOL_ID, APP_CLIENT_ID
from fastapi import Depends, HTTPException, Request, Security, status
from fastapi.security import HTTPBearer
from typing import Tuple
from utils.exceptions import RegionIsNotSet, UserPoolIdIsNotSet, AppClientIdIsNotSet
from utils.logger import log
from utils.pydant_model import AuthenticatedEntity


class CustomHTTPBearer(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        super().__init__(auto_error=auto_error)

    async def __call__(self, request: Request):
        try:
            return await super().__call__(request)
        except HTTPException as auth_exc:
            # Transform HTTP_403_FORBIDDEN to HTTP_401_UNAUTHORIZED
            if auth_exc.status_code == status.HTTP_403_FORBIDDEN:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Not authenticated",
                    headers={"WWW-Authenticate": "Bearer"},
                ) from auth_exc
            raise


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


def token_verifier(token: str = Security(CustomHTTPBearer())):
    """Verify the token using the TokenVerifier class.

    Args:
        token (str, optional): The token to be verified. Defaults to Depends(http_bearer).

    Raises:
        HTTPException: If the token is invalid, raise an HTTPException with status code 401.
    """
    # Verify if its in local and token is local
    verification = TokenVerifier(token.credentials)
    verify = verification.verify_token()
    if verify:
        return verification.claims
    log.debug(f"Token verification status: {verify}")
    if not verify:
        raise HTTPException(status_code=401, detail="Not authenticated")


def check_is_an_app(claims: dict) -> Tuple[bool, str]:
    scope = claims.get("scope")
    if scope:
        app_name = scope.split("/")[-1]
        log.info(f"App name: {app_name}")
        if len(app_name) > 0:
            return True, app_name
    return False, None


def is_a_local_authority(claims: dict) -> Tuple[bool, str]:
    username = claims.get("custom:local_authority")
    if username:
        return True, username
    return False, None


def operator(claims: dict = Depends(token_verifier)):
    return get_entity(claims, operator=True)


def read_only(claims: dict = Depends(token_verifier)):
    return get_entity(claims, read_only=True)


def get_local_authority(claims: dict = Depends(token_verifier)):
    return get_entity(claims, only_local_authority=True)


def get_group(claims: dict = Depends(token_verifier)):
    groups = claims.get("cognito:groups")
    if groups is None:
        raise HTTPException(
            status_code=401, detail="User is not part of any local authority group."
        )

    # Check if user is part of more than one group
    user_group_sum = sum("users-group" in group for group in groups)
    if user_group_sum > 1:
        raise HTTPException(
            status_code=422,
            detail="User is part of more than one local authority group.",
        )

    for group in groups:
        group_name = group.split("-")[-3]
        if "users-group" in group:
            return True, "user", group_name, claims.get("username")
        if "read-only" in group:
            return True, "read_only", group_name, claims.get("username")

    return False, None, None, None


def programmatic_access(claims: dict = Depends(token_verifier)):
    return get_entity(claims, is_an_app=True)


def operator_or_programmatic_access(claims: dict = Depends(token_verifier)):
    return get_entity(claims, operator=True, is_an_app=True)


def read_only_or_programmatic_access(claims: dict = Depends(token_verifier)):
    return get_entity(claims, read_only=True, is_an_app=True)


def get_entity(
    claims: dict = Depends(token_verifier),
    only_local_authority=False,
    operator=False,
    read_only=False,
    is_an_app=False,
) -> AuthenticatedEntity | HTTPException:
    """Check the identity weather its a local authority or an app.

    Args:
        claims (dict, optional): _description_. Defaults to Depends(token_verifier).

    Returns:
        AuthenticatedEntity: The current user/app, or raise an HTTPException with status code 401.
    """
    if is_an_app:
        is_app, app_name = check_is_an_app(claims)
        log.info(f"Is app: {is_app}")
        if is_app and len(app_name) > 0:
            return AuthenticatedEntity(type="app", name=app_name)

    if operator:
        has_group, type, group_name, user_name = get_group(claims)
        if not has_group:
            raise HTTPException(status_code=401, detail="Not authenticated")
        return AuthenticatedEntity(type=type, name=user_name, group=group_name)
    if read_only:
        has_group, type, group_name, user_name = get_group(claims)
        if type != "read_only":
            raise HTTPException(status_code=401, detail="Not authenticated")
        return AuthenticatedEntity(type=type, name=user_name, group=group_name)

    raise HTTPException(status_code=401, detail="Not authenticated")
