from peewee import *
import datetime

db = SqliteDatabase('orm_practise.db')


class BaseModel(Model):
    created_at = DateTimeField(default=datetime.datetime.now)
    uptated_at = DateTimeField(default=datetime.datetime.now)

    class Meta:
        database = db


class Store(BaseModel):
    name = CharField(unique=True)


class Warehouse(BaseModel):
    store = ForeignKeyField(Store, backref='warehouse')
    location = TextField()


class Product(BaseModel):
    name = CharField()
    description = TextField()
    warehouse = ForeignKeyField(Warehouse, backref='products')
