import pytest


@pytest.fixture(scope="module")
def vcr_config():
    """Configure VCR for API recording."""
    return {"filter_headers": ["Authorization"]}
