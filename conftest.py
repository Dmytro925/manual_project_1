import platform
from pathlib import Path

from pytest import Config, ExitCode, Session

from config.environments import get_api_base_url, get_base_url


def pytest_configure(config: Config) -> None:
    """Configure the application base URL for pytest."""
    config.option.base_url = get_base_url()


def pytest_sessionfinish(session: Session, exitstatus: ExitCode) -> None:
    """Save environment information for the Allure report."""
    alluredir = getattr(session.config.option, "allure_report_dir", None)
    if not alluredir:
        return
    results_dir = Path(alluredir)
    results_dir.mkdir(parents=True, exist_ok=True)

    browser = getattr(session.config.option, "browser", None) or ["chromium"]
    if isinstance(browser, (list, tuple)):
        browser = ",".join(browser)

    environment = {
        "Application URL": get_base_url(),
        "API URL": get_api_base_url(),
        "Browser": browser,
        "Python": platform.python_version(),
        "OS": platform.platform(),
    }

    content = "\n".join(
        f"{key}={value}" for key, value in environment.items()
    )
    (results_dir / "environment.properties").write_text(content)