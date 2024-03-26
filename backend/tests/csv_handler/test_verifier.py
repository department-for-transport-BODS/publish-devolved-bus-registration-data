from unittest.mock import MagicMock, patch
from auth.verifier import TokenVerifier, token_verifier
import pytest
from utils.exceptions import AppClientIdIsNotSet, RegionIsNotSet, UserPoolIdIsNotSet
from cognitojwt import CognitoJWTException
from fastapi import HTTPException


@patch("auth.verifier.AWS_REGION", "test_region")
@patch("auth.verifier.USERPOOL_ID", "test_userpool_id")
@patch("auth.verifier.APP_CLIENT_ID", "test_app_client_id")
@patch("cognitojwt.decode")
def test_verify_token_valid_token(mock_cognitojwt_decode):
    # Create a valid token
    token = "valid_token"
    # Create an instance of TokenVerifier
    verifier = TokenVerifier(token)
    verifier.verify_token()
    # mock_cognitojwt_decode.return_value = {"sub": "1234"}
    # assert verifier.token == "valid_token"
    mock_cognitojwt_decode.assert_called_once_with(
        "valid_token",
        "test_region",
        "test_userpool_id",
        app_client_id="test_app_client_id",
    )


@patch("auth.verifier.APP_CLIENT_ID", "APP_CLIENT_ID is not set")
def test_verify_token_missing_app_client_id():
    token = "valid_token"
    with pytest.raises(AppClientIdIsNotSet):
        verifier = TokenVerifier(token)
        verifier.verify_token()


@patch("auth.verifier.USERPOOL_ID", "USERPOOL_ID is not set")
def test_verify_token_missing_userpool_id():
    token = "valid_token"
    with pytest.raises(UserPoolIdIsNotSet):
        verifier = TokenVerifier(token)
        verifier.verify_token()


@patch("auth.verifier.AWS_REGION", "REGION is not set")
def test_verify_token_missing_region():
    token = "valid_token"
    with pytest.raises(RegionIsNotSet):
        verifier = TokenVerifier(token)
        verifier.verify_token()


@patch("auth.verifier.AWS_REGION", "test_region")
@patch("auth.verifier.USERPOOL_ID", "test_userpool_id")
@patch("auth.verifier.APP_CLIENT_ID", "test_app_client_id")
@patch("cognitojwt.decode")
@patch("auth.verifier.console.log")
def test_verify_token_invalid_token(mock_console_log, mock_cognitojwt_decode):
    # mock_cognitojwt_decode.side_effect = Exception("Invalid token")
    # Create an invalid token
    token = "invalid_token"
    # Create an instance of TokenVerifier
    verifier = TokenVerifier(token)
    # verifier.verify_token() is False
    # mock_console_log.assert_called_once_with(CognitoJWTException('Invalid token'))
    mock_cognitojwt_decode.side_effect = CognitoJWTException("Invalid token")
    assert verifier.verify_token() is False

    mock_cognitojwt_decode.side_effect = Exception("Invalid token")
    assert verifier.verify_token() is False

    # with patch("cognitojwt.decode", side_effect=Exception("Invalid token")):
    #     with pytest.raises(Exception) as e:
    #         verifier = TokenVerifier(token)
    #         verify = verifier.verify_token()
    # # assert verify is True


@patch("auth.verifier.PROJECT_ENV", "localdev")
def test_token_verifier_valid_token():
    # Arrange
    token = MagicMock()
    token.credentials = "localdev"
    assert token_verifier(token) is None
    # Acit
    # Asisert


@patch("auth.verifier.log.debug")
@patch("auth.verifier.TokenVerifier.verify_token", return_value=False)
def test_token_verifier_invalid_token(mock_verify_token, mock_log):
    # Arrange
    token = MagicMock()
    token.credentials = "invalid"
    with pytest.raises(HTTPException):
        token_verifier(token)
    mock_log.assert_called_once_with("Token verification status: False")
    # Acit
    # Asisert
