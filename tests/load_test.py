import pytest
from models import Services
from sqlmodel import Session


def test_divisible_by_3(input_value):
    assert input_value % 3 == 0


def test_divisible_by_6(input_value):
    assert input_value % 6 == 0


def test_db(session: Session):
    services = session.query(Services).all()
    assert len(services) == 0
