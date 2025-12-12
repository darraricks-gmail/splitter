import os
import shutil
from datetime import datetime

import pytest

from constants import TESTS_DIR, ARTIFACTS_DIR

@pytest.fixture(scope="session")
def test_run_timestamp():
  return datetime.now().strftime("%Y%m%d_%H%M%S")

def pytest_sessionstart():
    os.makedirs("test_artifacts", exist_ok=True)

def pytest_terminal_summary():
    shutil.copy(TESTS_DIR / "report.html", ARTIFACTS_DIR / "report.html")
    shutil.copy(TESTS_DIR / "test_results.xml", ARTIFACTS_DIR / "test_results.xml")

