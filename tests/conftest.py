import pytest
from db import clean_up_db, init_connection_pool, migrate_db
from sqlmodel import Session


@pytest.fixture
def input_value():
    input = 36
    return input


@pytest.fixture
def session():
    def setup():
        engine = init_connection_pool()
        clean_up_db(engine)
        migrate_db(engine)
        return engine

    pool = setup()
    with Session(pool) as session:
        yield session

    clean_up_db(pool)
    pool.dispose()
