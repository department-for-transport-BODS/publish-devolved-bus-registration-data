from unittest.mock import patch
from os import environ
import json
from assets.validotcresponses import (
    VALID_AUTH_RESPONSE,
    VALID_RESPONSES,
    EXPECTED_OUTPUTS,
)

environ["MS_LOGIN_URL"] = "https://example.com"
environ["MS_TENANT_ID"] = "testid"
environ["OTC_API_KEY"] = "testkey"
environ["OTC_API_URL"] = "https://example.com"

from otcclient.otcclient import OTCAuthenticator, lambda_handler


def test_authenticator_success(requests_mock):
    requests_mock.post(
        "https://example.com/testid/oauth2/v2.0/token", json=VALID_AUTH_RESPONSE
    )
    authenticator = OTCAuthenticator()
    assert authenticator.token == VALID_AUTH_RESPONSE["access_token"]


def test_authenticator_fail(requests_mock, caplog):
    requests_mock.post("https://example.com/testid/oauth2/v2.0/token", status_code=400)
    returned_output = lambda_handler(["NOTAVALIDLICENCE"], None)
    assert returned_output["statusCode"] == 400
    assert "Couldn't fetch Authorization token" in caplog.text


def test_otc_requests(requests_mock):
    for licence, return_values in VALID_RESPONSES.items():
        requests_mock.get(
            f"https://example.com/?limit=1&page=1&licenceNo={licence}&latestVariation=true",
            json=return_values,
        )
    requests_mock.get(
        "https://example.com/?limit=1&page=1&licenceNo=NOTAVALIDLICENCE&latestVariation=true",
        status_code=204,
    )
    test_licence_numbers = [
        licence["licence_number"] for licence in EXPECTED_OUTPUTS["licences"]
    ]
    with patch("otcclient.otcclient.OTCAuthenticator"):
        returned_output = lambda_handler(test_licence_numbers, None)

        assert sorted(
            json.loads(returned_output["body"])["licences"],
            key=lambda x: x["licence_number"],
        ) == sorted(EXPECTED_OUTPUTS["licences"], key=lambda y: y["licence_number"])


def test_invalid_input():
    response = lambda_handler("not a list", None)
    assert response.get("statusCode", None) == 400


def test_malformed_response(requests_mock, caplog):

    expected_output = {
        "licences": [
            {
                "licence_details": None,
                "licence_number": "NOTAVALIDLICENCE",
                "operator_details": None,
            }
        ]
    }

    requests_mock.get(
        "https://example.com/?limit=1&page=1&licenceNo=NOTAVALIDLICENCE&latestVariation=true",
        json={"notBus": None},
    )
    with patch("otcclient.otcclient.OTCAuthenticator"):
        returned_output = lambda_handler(["NOTAVALIDLICENCE"], None)
        assert "no busSearch component" in caplog.text
        assert json.loads(returned_output["body"]) == expected_output

    requests_mock.get(
        "https://example.com/?limit=1&page=1&licenceNo=NOTAVALIDLICENCE&latestVariation=true",
        json={"busSearch": []},
    )
    with patch("otcclient.otcclient.OTCAuthenticator"):
        returned_output = lambda_handler(["NOTAVALIDLICENCE"], None)
        assert "busSearch component contains no record" in caplog.text
        assert json.loads(returned_output["body"]) == expected_output

    requests_mock.get(
        "https://example.com/?limit=1&page=1&licenceNo=NOTAVALIDLICENCE&latestVariation=true",
        json={"busSearch": [{"licenceNumber": "NOTAVALIDLICENCE"}]},
    )
    with patch("otcclient.otcclient.OTCAuthenticator"):
        returned_output = lambda_handler(["NOTAVALIDLICENCE"], None)
        assert "validation error" in caplog.text
        assert "for OTCLicence" in caplog.text
        assert "for Operator" in caplog.text
        assert json.loads(returned_output["body"]) == expected_output


# def test_invalid_path(requests_mock):
#     requests_mock.get(DATA_CATALOGUE_URL, exc=requests.exceptions.HTTPError)
#     with patch("bodsdatacatalogue.datacatalogue.Session"):
#         with pytest.raises(requests.exceptions.HTTPError):
#             lambda_handler(None, None)


# def test_invalid_zipfile(requests_mock):
#     requests_mock.get(DATA_CATALOGUE_URL, content=b"Not a zip")
#     with patch("bodsdatacatalogue.datacatalogue.Session"):
#         with pytest.raises(BadZipFile):
#             lambda_handler(None, None)


# def test_missing_file(requests_mock):
#     requests_mock.get(DATA_CATALOGUE_URL, content=open(text_zip_path, "rb").read())
#     with patch("bodsdatacatalogue.datacatalogue.Session"):
#         with pytest.raises(KeyError):
#             lambda_handler(None, None)


# def test_valid_file(requests_mock):
#     requests_mock.get(DATA_CATALOGUE_URL, content=open(valid_zip_path, "rb").read())
#     with patch("bodsdatacatalogue.datacatalogue.Session"):
#         try:
#             lambda_handler(None, None)
#         except Exception as e:
#             pytest.fail(f"Failed to refresh database {e}")
