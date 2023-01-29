import pytest
from db import clean_up_db, init_connection_pool, migrate_db
from sqlmodel import Session


@pytest.fixture
def input_value():
    input = 36
    return input


@pytest.fixture(scope="module")
def session():
    engine = init_connection_pool()
    clean_up_db(engine)
    migrate_db(engine)

    with Session(engine) as session:
        yield session

    clean_up_db(engine)
    engine.dispose()
