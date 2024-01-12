import sqlalchemy
from sqlalchemy.orm import sessionmaker
import json

from models import create_tables, Publisher, Book, Shop, Stock, Sale
from login import db_login, db_name, db_pass


def create_db(data):
    DSN = f'postgresql://{db_login}:{db_pass}@localhost:5432/{db_name}'
    engine = sqlalchemy.create_engine(DSN)
    create_tables(engine)

    Session = sessionmaker(bind=engine)
    session = Session()

    for record in data:
        model = {
            'publisher': Publisher,
            'shop': Shop,
            'book': Book,
            'stock': Stock,
            'sale': Sale,
        }[record.get('model')]
        session.add(model(id=record.get('pk'), **record.get('fields')))
    session.commit()

    session.close()


def read_file():
    with open("files/tests_data.json", encoding="utf-8") as file:
        data_from_file = json.load(file)
    return data_from_file


if __name__ == "__main__":
    create_db(read_file())
