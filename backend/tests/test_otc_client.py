from unittest.mock import patch
from os import environ
import pytest

# Set env vars BEFORE importing the app so getenv() picks them up at module load time
environ["MS_LOGIN_URL"] = "https://example.com"
environ["MS_TENANT_ID"] = "testid"
environ["OTC_API_KEY"] = "testkey"
environ["OTC_API_URL"] = "https://example.com"

from fastapi.testclient import TestClient
from src.otc_client.app import OTCAuthenticator, app


from assets.validotcresponses import (
    VALID_AUTH_RESPONSE,
    VALID_RESPONSES,
    EXPECTED_OUTPUTS,
)

environ["MS_LOGIN_URL"] = "https://example.com"
environ["MS_TENANT_ID"] = "testid"
environ["OTC_API_KEY"] = "testkey"
environ["OTC_API_URL"] = "https://example.com"


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
            f"https://example.com/?limit=1&page=1&identifier={licence}&latestVariation=true",
            json=return_values,
        )
    requests_mock.get(
        "https://example.com/?limit=1&page=1&identifier=NOTAVALIDLICENCE&latestVariation=true",
        status_code=204,
    )
    test_licence_numbers = [
        licence["licence_number"] for licence in EXPECTED_OUTPUTS["licences"]
    ]
    with patch("src.otc_client.app.OTCAuthenticator"):
        returned_output = client.post("/api/v1/otc/licences", json=test_licence_numbers)

        assert sorted(
            returned_output.json()["licences"],
            key=lambda x: x["licence_number"],
        ) == sorted(EXPECTED_OUTPUTS["licences"], key=lambda y: y["licence_number"])


def test_invalid_input():
    response = client.post("/api/v1/otc/licences", json="not a list")
    assert response.status_code == 422


_expected_none = {
    "licences": [{"licence_details": None, "licence_number": "NOTAVALIDLICENCE", "operator_details": None}]
}

@pytest.mark.parametrize(
    "mock_json, expected_status, expected_log, expected_output",
    [
        pytest.param(
            {"notReport": None},
            400, None, None,
            id="missing_report_key",
        ),
        pytest.param(
            {"report": None},
            400, None, None,
            id="report_is_none",
        ),
        pytest.param(
            {"report": {}},
            200, "no licenceDetails component", _expected_none,
            id="missing_licence_details_key",
        ),
        pytest.param(
            {"report": {"licenceDetails": []}},
            200, "licenceDetails component contains no records", _expected_none,
            id="empty_licence_details",
        ),
        pytest.param(
            {"report": {"licenceDetails": [{"licenceNumber": "NOTAVALIDLICENCE"}]}},
            200, "Could not get operator detail",
            {
                "licences": [
                    {
                        "licence_details": {"licence_number": "NOTAVALIDLICENCE", "licence_status": None},
                        "licence_number": "NOTAVALIDLICENCE",
                        "operator_details": None,
                    }
                ]
            },
            id="missing_operator_fields",
        ),
    ],
)
def test_malformed_response(requests_mock, caplog, mock_json, expected_status, expected_log, expected_output):
    requests_mock.get(
        "https://example.com/?limit=1&page=1&identifier=NOTAVALIDLICENCE&latestVariation=true",
        json=mock_json,
    )
    with patch("src.otc_client.app.OTCAuthenticator"):
        returned_output = client.post("/api/v1/otc/licences", json=["NOTAVALIDLICENCE"])
        assert returned_output.status_code == expected_status
        if expected_log:
            assert expected_log in caplog.text
        if expected_output:
            assert returned_output.json() == expected_output
