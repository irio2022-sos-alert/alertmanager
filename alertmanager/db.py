import os

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlmodel import SQLModel

load_dotenv()  # take environment variables from .env.

POSTGRES_USER = os.getenv("POSTGRES_USER")
POSTGRES_PWD = os.getenv("POSTGRES_PWD")
POSTGRES_HOST = os.getenv("POSTGRES_HOST")
POSTGRES_PORT = os.getenv("POSTGRES_PORT")
DB_NAME = "bd"

db_url = f"postgresql://{POSTGRES_USER}:{POSTGRES_PWD}@{POSTGRES_HOST}/{DB_NAME}"

engine = create_engine(db_url)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


def clean_up_db():
    SQLModel.metadata.drop_all(engine)
