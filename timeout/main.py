from datetime import timedelta

from prefect import Flow, task
from prefect.schedules import IntervalSchedule

schedule = IntervalSchedule(interval=timedelta(seconds=5))


@task
def say_hello():
    print("hello")


with Flow("Hello Flow", schedule=schedule) as flow:
    say_hello()

if __name__ == "__main__":
    flow.run()
