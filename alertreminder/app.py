import logging
from multiprocessing import Process

from flask import Flask
from main import background_task

app = Flask(__name__)

logging.basicConfig(level=logging.INFO)


@app.route("/")
def home():
    return "Background task running"


p = Process(target=background_task)
p.start()

if __name__ == "__main__":
    app.run(debug=True)
