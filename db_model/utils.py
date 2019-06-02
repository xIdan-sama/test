import json
import datetime
from decimal import Decimal


DATE_FORMAT = '%Y-%m-%d'
TIME_FORMAT = '%H:%M:%S'
DATETIME_FORMAT = '{} {}'.format(DATE_FORMAT, TIME_FORMAT)


class JsonEncoder(json.JSONEncoder):
    def default(self, o):
        """
        Метод подготовки нестандартных типов данных для сериализации.

        :param o: объект сериализации

        :return: объект, содержащий в себе простые типы данных,
                 пригодные для сериализации
        """
        # порядок проверки на datetime, date важен!
        if isinstance(o, datetime.datetime):
            return o.strftime(DATETIME_FORMAT)
        elif isinstance(o, datetime.date):
            return o.strftime(DATE_FORMAT)
        if isinstance(o, Decimal):
            return float(o)

        super().default(o)
