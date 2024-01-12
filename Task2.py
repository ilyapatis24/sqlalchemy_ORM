import sqlalchemy
from sqlalchemy.orm import sessionmaker
import json

from models import create_tables, Publisher, Book, Shop, Stock, Sale
from login import db_login, db_name, db_pass


def id_or_name(value):
    try:
        result = int(value)
        return result
    except ValueError:
        return value


def session_open(flag=True):
    DSN = f'postgresql://{db_login}:{db_pass}@localhost:5432/{db_name}'
    engine = sqlalchemy.create_engine(DSN)
    if flag:
        create_tables(engine)

    Session = sessionmaker(bind=engine)
    return Session()


def create_db(data):
    session = session_open()

    for item in data:
        if item['model'] == 'publisher':
            publisher = Publisher(
                name=item['fields']['name'],
                id=item['pk'])
            session.add(publisher)

        elif item['model'] == 'book':
            book = Book(
                id=item['pk'],
                title=item['fields']['title'],
                id_publisher=item['fields']['id_publisher'])
            session.add(book)

        elif item['model'] == 'shop':
            shop = Shop(
                id=item['pk'],
                name=item['fields']['name'])
            session.add(shop)

        elif item['model'] == 'stock':
            stock = Stock(
                id=item['pk'],
                id_book=item['fields']['id_book'],
                id_shop=item['fields']['id_shop'],
                count=item['fields']['count'])
            session.add(stock)

        elif item['model'] == 'sale':
            sale = Sale(
                id=item['pk'],
                price=item['fields']['price'],
                date_sale=item['fields']['date_sale'],
                id_stock=item['fields']['id_stock'],
                count=item['fields']['count'])
            session.add(sale)
        session.commit()
    session.close()


def sale_facts(ask_publisher):
    session = session_open(False)
    ask_publisher = id_or_name(ask_publisher)
    if type(ask_publisher) == str:
        id_publisher = session.query(Publisher.id).filter(Publisher.name == ask_publisher).scalar()
    else:
        id_publisher = ask_publisher
    if id_publisher:
        for item in session.query(Book.title, Shop.name, Sale.price, Sale.date_sale).join(Sale.stock)\
                .join(Stock.shop).join(Stock.book).filter(Book.id_publisher == id_publisher).all():
            print_list = list(item)
            print(f"{print_list[0]:<20}|\t"
                  f"{print_list[1]:<15}|\t"
                  f"{int(print_list[2]):<9}|\t"
                  f"{print_list[3].strftime('%d-%m-%Y')}")
    else:
        print('Publisher not found')

    session.close()


def read_file():
    with open("files/tests_data1.json", encoding="utf-8") as file:
        data_from_file = json.load(file)
    return data_from_file


if __name__ == "__main__":
    create_db(read_file())
    sale_facts(input('Enter publisher name(or id): '))
