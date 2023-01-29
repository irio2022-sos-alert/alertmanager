import os
from multiprocessing import Process

from flask import Flask
from main import background_task

app = Flask(__name__)

task_started_file = "task_started.txt"


@app.route("/")
def home():
    return "Background task running"


if not os.path.exists(task_started_file):
    p = Process(target=background_task)
    p.start()
    with open(task_started_file, "w") as f:
        f.write("task started")

if __name__ == "__main__":
    app.run(debug=True)
