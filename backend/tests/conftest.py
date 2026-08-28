import pytest
from backend.repositories.financial_repository import repo


@pytest.fixture(autouse=True)
def reset_repository_state():
    """
    Ensure each test runs with a fresh, clean in-memory repository state.
    """
    repo.reset()
    yield
    repo.reset()
