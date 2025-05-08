import os
import pytest
from click.testing import CliRunner

FILE_PATH = "sample_file/main.cpp"


@pytest.fixture(scope='session')
def cli_resources():
    cli_runner = CliRunner()
    yield cli_runner


@pytest.fixture(scope='session')
def pm_token():
    api_key = os.getenv("PRODUCT_MAP_TOKEN", None)
    return api_key
