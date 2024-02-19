import pytest
from unittest.mock import patch
import requests
from os import path
from bodsdatacatalogue.datacatalogue import DATA_CATALOGUE_URL, lambda_handler
from zipfile import BadZipFile

test_script_path = path.dirname(path.abspath(__file__))
text_zip_path = path.join(test_script_path, "assets", "text.zip")
valid_zip_path = path.join(test_script_path, "assets", "valid_catalogue.zip")

def test_invalid_path(requests_mock):
    requests_mock.get(DATA_CATALOGUE_URL, exc=requests.exceptions.HTTPError)
    with patch("bodsdatacatalogue.datacatalogue.Session"):
        with pytest.raises(requests.exceptions.HTTPError):
            lambda_handler(None, None)


def test_invalid_zipfile(requests_mock):
    requests_mock.get(DATA_CATALOGUE_URL, content=b"Not a zip")
    with patch("bodsdatacatalogue.datacatalogue.Session"):
        with pytest.raises(BadZipFile):
            lambda_handler(None, None)


def test_missing_file(requests_mock):
    requests_mock.get(
        DATA_CATALOGUE_URL, content=open(text_zip_path, "rb").read()
    )
    with patch("bodsdatacatalogue.datacatalogue.Session"):
        with pytest.raises(KeyError):
            lambda_handler(None, None)

def test_valid_file(requests_mock):

    requests_mock.get(
        DATA_CATALOGUE_URL, content=open(valid_zip_path, "rb").read()
    )
    with patch("bodsdatacatalogue.datacatalogue.Session"):
        try:
            lambda_handler(None, None)
        except Exception as e:
            pytest.fail(f'Failed to refresh database {e}')