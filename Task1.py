import sqlalchemy
from sqlalchemy.orm import sessionmaker
import json

from models import create_tables
from login import db_login, db_name, db_pass


def create_db():
    DSN = f'postgresql://{db_login}:{db_pass}@localhost:5432/{db_name}'
    engine = sqlalchemy.create_engine(DSN)
    create_tables(engine)

    Session = sessionmaker(bind=engine)
    session = Session()

    session.close()


def read_file():
    with open("files/tests_data.json", encoding="utf-8") as file:
        data_from_file = json.load(file)
    return data_from_file


if __name__ == "__main__":
    create_db()
