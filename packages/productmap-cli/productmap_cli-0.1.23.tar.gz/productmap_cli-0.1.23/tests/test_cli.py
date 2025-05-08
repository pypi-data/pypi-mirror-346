from cli.main import main

from tests.conftest import FILE_PATH


def test_without_parameters(cli_resources):
    result = cli_resources.invoke(main)
    assert result.exit_code == 2
    assert "missing argument" in result.output.lower()


def test_validate_file(cli_resources, pm_token):
    result = cli_resources.invoke(main, [pm_token, "--file", FILE_PATH, "--action", "validate"])
    assert result.exit_code == 0
    assert "validated successfully" in result.output.lower()


def test_generate_map(cli_resources, pm_token):
    result = cli_resources.invoke(main, [pm_token, "--file", FILE_PATH, "--action", "generate"])
    assert result.exit_code == 0
    assert "mapped with salt:" in result.output.lower()


def test_invalid_action(cli_resources, pm_token):
    result = cli_resources.invoke(main, [pm_token, "--file", FILE_PATH, "--action", "invalid"])
    assert result.exit_code == 2
    assert "invalid value for '--action'" in result.output.lower()