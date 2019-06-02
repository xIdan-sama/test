import json

from peewee import *

from db_model import utils


pg_db = PostgresqlDatabase(
    'test',
    user='test_user',
    password='test_password'
)


class BaseModel(Model):
    def __str__(self):
        return json.dumps(self.__data__, cls=utils.JsonEncoder)

    class Meta:
        database = pg_db


class StockPricesModel(BaseModel):
    rn = PrimaryKeyField(null=False)
    company = CharField(max_length=50, null=False)
    date = DateField(null=False)
    open = DecimalField(max_digits=14, decimal_places=4, null=False)
    high = DecimalField(max_digits=14, decimal_places=4, null=False)
    low = DecimalField(max_digits=14, decimal_places=4, null=False)
    close = DecimalField(max_digits=14, decimal_places=4, null=False)
    volume = IntegerField(null=False)

    class Meta:
        db_table = 'stock_prices'
        indexes = (
            (('company', 'date'), True),
            (('company',), False),
            (('date',), False)
        )


class InsidersModel(BaseModel):
    rn = PrimaryKeyField(null=False)
    company = CharField(max_length=50, null=False)
    name = CharField(max_length=255, null=False)
    relation = CharField(max_length=150, null=False)

    class Meta:
        db_table = 'insiders'
        indexes = (
            (('company', 'name'), True),
            (('company',), False)
        )


class TradesModel(BaseModel):
    rn = PrimaryKeyField(null=False)
    insider = ForeignKeyField(InsidersModel, db_column='insider', null=False)
    date = DateField(null=False)
    type = CharField(max_length=255, null=False)
    owner_type = CharField(max_length=25, null=False)
    traded = IntegerField(null=False)
    price = DecimalField(max_digits=14, decimal_places=4, null=False)
    held = IntegerField(null=False)

    class Meta:
        db_table = 'trades'
        indexes = (
            (('insider',), False)
        )
