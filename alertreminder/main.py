import logging
import os
import sys
from datetime import datetime, timedelta, timezone

import alert_pb2
import alert_pb2_grpc
import grpc
import psutil
from db import init_connection_pool, migrate_db
from models import Alerts
from prefect import Flow, task
from prefect.schedules import IntervalSchedule
from sqlmodel import Session


def make_deadline_notification(alert: Alerts) -> alert_pb2.AlertRequest:
    return alert_pb2.AlertRequest(serviceId=alert.service_id)


def init_db():
    global engine
    engine = init_connection_pool()
    migrate_db(engine)


@task
def getExpiredAlerts():
    with Session(engine) as session:
        now = datetime.now(timezone.utc)
        expired_alerts = session.query(Alerts).where(Alerts.deadline < now).all()
        logging.info(f"Found expired alerts: {len(expired_alerts)}")
        return expired_alerts


@task
def notify(expired_alerts: list[Alerts], endpoint: str) -> None:
    with grpc.secure_channel(endpoint, grpc.ssl_channel_credentials()) as channel:
        stub = alert_pb2_grpc.AlertManagerStub(channel)
        for alert in expired_alerts:
            notification = make_deadline_notification(alert)
            response = stub.HandleResponseDeadline(notification)
            logging.info(
                f"""Notified {endpoint} about expired alert for service {id},
            received status = {response.okay} and message : {response.message}"""
            )


with Flow("Response deadline ticker") as flow:
    logging.info(f"Running flow from process with pid {os.getpid()}")
    endpoint = os.getenv("ALERTMANAGER_ENDPOINT", "localhost:50052")
    expired_alerts = getExpiredAlerts()
    notify(expired_alerts, endpoint)


def kickoff_auto_heal(task, old_state, new_state):
    if new_state.is_failed():
        logging.info(
            f"Background task with pid {os.getpid()} has failed, killing parent and commencing autoheal."
        )
        p = psutil.Process(os.getppid())
        p.terminate()  # or p.kill()
        sys.exit()


def background_task():
    init_db()
    interval = os.getenv("TIMEDELTA", 20)
    schedule = IntervalSchedule(interval=timedelta(seconds=interval))
    flow.schedule = schedule
    flow.state_handlers = [kickoff_auto_heal]
    logging.info(f"Staring flow with interval: {interval}")
    flow.run()


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    background_task()
