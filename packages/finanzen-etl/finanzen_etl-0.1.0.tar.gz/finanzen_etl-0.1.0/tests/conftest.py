"""
Configuration file for pytest fixtures and hooks.
"""
import pytest

# Example fixture (can be removed or modified)


@pytest.fixture(scope="session")
def example_session_fixture():
    print("\nSetting up session fixture...")
    yield
    print("\nTearing down session fixture...")
