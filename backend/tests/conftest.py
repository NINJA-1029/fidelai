import sys
from pathlib import Path
import pytest

# Ensure repository root is on sys.path for test discovery
project_root = Path(__file__).resolve().parent.parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

from backend.repositories.financial_repository import repo


@pytest.fixture(autouse=True)
def reset_repository_state():
    """
    Ensure each test runs with a fresh, clean in-memory repository state.
    """
    repo.reset()
    yield
    repo.reset()

