import os
import time

import pytest
import requests
from models import Alerts, Services
from requests import Response
from sqlmodel import Session
from utils import call_datamanager_api


def test_divisible_by_3(input_value):
    assert input_value % 3 == 0


def test_divisible_by_6(input_value):
    assert input_value % 6 == 0


@pytest.fixture(autouse=True, scope="module")
def test_api_config_change(session):
    endpoint = os.environ["API_ENDPOINT"]
    r1 = call_datamanager_api(
        endpoint=endpoint,
        service_name="google",
        service_url="google.com",
        frequency=3,
        alerting_window=5,
        allowed_resp_time=10000,
        email1="john.doe@gmail.com",
        email2="john.boyle@gmail.com",
    )

    r2 = call_datamanager_api(
        endpoint=endpoint,
        service_name="broken",
        service_url="com.com",
        frequency=3,
        alerting_window=5,
        allowed_resp_time=10000,
        email1="john.doe@gmail.com",
        email2="john.boyle@gmail.com",
    )
    assert r1.status_code == 200
    assert r2.status_code == 200


def test_persisting_config(session: Session):
    services = session.query(Services).all()
    assert len(services) == 2


def test_raising_alerts(session: Session):
    time.sleep(60)
    alerts = session.query(Alerts).all()
    assert len(alerts) == 1
