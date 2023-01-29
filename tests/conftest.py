import pytest
from db import init_connection_pool, migrate_db
from sqlmodel import Session


@pytest.fixture
def input_value():
    input = 36
    return input


@pytest.fixture
def session():
    pool = init_connection_pool()
    migrate_db(pool)
    with Session(pool) as session:
        yield session
