from typing import Generator

import pytest
from fastapi.testclient import TestClient

from app.core.application import get_app


@pytest.fixture(scope='module')
def client() -> Generator:
    api = get_app()
    with TestClient(api) as c:
        yield c
