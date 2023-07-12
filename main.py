import sqlalchemy
from sqlalchemy.orm import sessionmaker
import json

from models import create_tables, Publisher, Sale, Book, Stock, Shop

SQL_system = 'postgresql'
login = 'postgres'
password = '192837465'
host = 'localhost'
port = 5432
db_name = 'postgres'

DSN = f'{SQL_system}://{login}:{password}@{host}:{port}/{db_name}'
engine = sqlalchemy.create_engine(DSN)

Session = sessionmaker(bind=engine)
session = Session()

create_tables(engine)

with open('test_data.json', 'r') as f:
    test_data = json.load(f)

model = {
    'publisher': Publisher,
    'book': Book,
    'shop': Shop,
    'stock': Stock,
    'sale': Sale
}

for item in test_data:
    model_name = item['model']
    model_class = model.get(model_name)

    if model_class:
        fields = item['fields']
        model_inst = model_class(**fields)
        session.add(model_inst)


# with open('test_data.json', 'r') as db:
#     data = json.load(db)

# for line in data:
#     method = {
#         'publisher': Publisher,
#         'shop': Shop,
#         'book': Book,
#         'stock': Stock,
#         'sale': Sale,
#     }[line['model']]
#     session.add(method(id=line['pk'], **line.get('fields')))

session.commit()

publisher_name = input('Введите имя писателя или id для вывода: ')

def search(param):
    publ_name = session.query(Publisher).filter(param == publisher_name).first()
    query = session.query(Book.title, Shop.name, Sale.price, Sale.date_sale).\
        join(Stock, Book.id == Stock.id_book).\
        join(Sale, Stock.id == Sale.id_stock).\
        join(Shop, Stock.id_shop == Shop.id).\
        filter(Book.id_publisher == publ_name.id)
    for title, shop_name, price, date_sale in query:
        print(f'{title} | {shop_name} | {price} | {date_sale}')
    

try:
    if publisher_name.isnumeric():
        search(Publisher.id)
    else:
        search(Publisher.name)
except:
    print("Писателя с таким именем или id не существует")


session.close()
