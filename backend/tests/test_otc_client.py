from unittest.mock import patch
from os import environ
import json
from fastapi.testclient import TestClient


from assets.validotcresponses import (
    VALID_AUTH_RESPONSE,
    VALID_RESPONSES,
    EXPECTED_OUTPUTS,
)

environ["MS_LOGIN_URL"] = "https://example.com"
environ["MS_TENANT_ID"] = "testid"
environ["OTC_API_KEY"] = "testkey"
environ["OTC_API_URL"] = "https://example.com"

from src.otcclient.app import OTCAuthenticator, app

client = TestClient(app)


def test_authenticator_success(requests_mock):
    requests_mock.post(
        "https://example.com/testid/oauth2/v2.0/token", json=VALID_AUTH_RESPONSE
    )
    authenticator = OTCAuthenticator()
    assert authenticator.token == VALID_AUTH_RESPONSE["access_token"]


def test_authenticator_fail(requests_mock, caplog):
    requests_mock.post("https://example.com/testid/oauth2/v2.0/token", status_code=400)
    returned_output = client.post("/api/v1/otc/licences", json=["NOTAVALIDLICENCE"])
    assert returned_output.status_code == 400
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
    with patch("src.otcclient.app.OTCAuthenticator"):
        returned_output = client.post("/api/v1/otc/licences", json=test_licence_numbers)

        assert sorted(
            returned_output.json()["licences"],
            key=lambda x: x["licence_number"],
        ) == sorted(EXPECTED_OUTPUTS["licences"], key=lambda y: y["licence_number"])


def test_invalid_input():
    response = client.post("/api/v1/otc/licences", json="not a list")
    assert response.status_code == 422


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
    with patch("src.otcclient.app.OTCAuthenticator"):
        returned_output = client.post("/api/v1/otc/licences", json=["NOTAVALIDLICENCE"])
        assert "no busSearch component" in caplog.text
        assert returned_output.json() == expected_output

    requests_mock.get(
        "https://example.com/?limit=1&page=1&licenceNo=NOTAVALIDLICENCE&latestVariation=true",
        json={"busSearch": []},
    )
    with patch("src.otcclient.app.OTCAuthenticator"):
        returned_output = client.post("/api/v1/otc/licences", json=["NOTAVALIDLICENCE"])
        assert "busSearch component contains no record" in caplog.text
        assert returned_output.json() == expected_output

    requests_mock.get(
        "https://example.com/?limit=1&page=1&licenceNo=NOTAVALIDLICENCE&latestVariation=true",
        json={"busSearch": [{"licenceNumber": "NOTAVALIDLICENCE"}]},
    )
    with patch("src.otcclient.app.OTCAuthenticator"):
        returned_output = client.post("/api/v1/otc/licences", json=["NOTAVALIDLICENCE"])
        assert "validation error" in caplog.text
        assert "for OTCLicence" in caplog.text
        assert "for Operator" in caplog.text
        assert returned_output.json() == expected_output
