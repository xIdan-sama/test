from peewee import fn

from db_model.base import StockPricesModel, InsidersModel, TradesModel, pg_db


def index():
    return StockPricesModel.select(StockPricesModel.company).group_by(StockPricesModel.company)


def ticker_get(ticker):
    return StockPricesModel.select().where(StockPricesModel.company == ticker)


def insider_get(ticker):
    return TradesModel.select().join(InsidersModel).where(InsidersModel.company == ticker)


def insider_item(ticker, name):
    return TradesModel.select().join(InsidersModel).where(InsidersModel.company == ticker, InsidersModel.name == name)


def analytics(args, ticker):
    start, end = StockPricesModel.select(
        fn.Min(StockPricesModel.date), fn.Max(StockPricesModel.date)
    ).where(StockPricesModel.date >= args['date_from'], StockPricesModel.date <= args['date_to']).scalar(as_tuple=True)

    self = StockPricesModel.alias()
    res = StockPricesModel.select(
        self.open - StockPricesModel.open,
        self.high - StockPricesModel.high,
        self.low - StockPricesModel.low,
        self.close - StockPricesModel.close
    ).join(self, on=True).where(
        StockPricesModel.company == ticker,
        StockPricesModel.date == start,
        self.company == ticker,
        self.date == end
    ).scalar(as_tuple=True)

    return res


def delta(args, ticker):
    cursor = pg_db.execute_sql('SELECT delta(%s, %s, %s)', (ticker, args['value'], args['type']))
    row = cursor.fetchone()
    return [row[0][1:-1].replace(',', ' - ')]
