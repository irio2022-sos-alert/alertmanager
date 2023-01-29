import os
import time

import pytest
from models import Services
from sqlmodel import Session
from utils import call_datamanager_api


@pytest.fixture(scope="module")
def services_count():
    return 1000


def test_populate_config(services_count):
    endpoint = os.environ["API_ENDPOINT"]
    status_code_counter = 0

    for i in range(services_count):
        response = call_datamanager_api(
            endpoint=endpoint,
            service_name=f"test_service_{i}",
            service_url=".com.com",
            frequency=3,
            alerting_window=5,
            allowed_resp_time=10000,
            email1="john.doe@gmail.com",
            email2="john.boyle@gmail.com",
        )

        if response.status_code == 200:
            status_code_counter += 1

    assert status_code_counter == services_count


def test_rasing_alerts(session: Session, services_count):
    time.sleep(60)
    services = session.query(Services).all()
    assert len(services) == services_count
