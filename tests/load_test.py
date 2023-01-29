import os
import time

import pytest
from models import Admins, Ownership, Services
from sqlmodel import Session
from utils import call_datamanager_api


@pytest.fixture(scope="module")
def services_count():
    return 1000


# def test_populate_config(services_count):
#     endpoint = os.environ["API_ENDPOINT"]
#     status_code_counter = 0

#     for i in range(services_count):
#         response = call_datamanager_api(
#             endpoint=endpoint,
#             service_name=f"test_service_{i}",
#             service_url=".com.com",
#             frequency=3,
#             alerting_window=5,
#             allowed_resp_time=10000,
#             email1="john.doe@gmail.com",
#             email2="john.boyle@gmail.com",
#         )

#         if response.status_code == 200:
#             status_code_counter += 1

#     assert status_code_counter == services_count


def test_populate_config(session: Session, services_count):
    print("hello")
    admin1 = Admins(id=1, email="john.doe@gmail.com")
    admin2 = Admins(id=2, email="john.doe@gmail.com")
    session.add(admin1)
    session.add(admin2)

    services = []

    for i in range(services_count):
        service = Services(
            id=i,
            name=f"test_service_{i}",
            domain=".com.com",
            frequency=3,
            alerting_window=5,
            allowed_response_time=1000,
        )
        session.add(service)
        services.append(service)

    print("hello")

    session.commit()

    print("hello")
    for service in services:
        session.add(
            Ownership(service_id=service.id, admin_id=admin1.id, first_contact=True)
        )
        session.add(
            Ownership(service_id=service.id, admin_id=admin2.id, first_contact=False)
        )

    print("hello")
    session.commit()
    print("hello")

    assert len(session.query(Services).all()) == services_count


def test_db(session: Session, services_count):
    time.sleep(60)
    services = session.query(Services).all()
    assert len(services) == services_count
