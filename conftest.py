from pytest import Config

from config.environments import get_base_url


def pytest_configure(config: Config) -> None:
    """Configure the application base URL for pytest."""
    config.option.base_url = get_base_url()