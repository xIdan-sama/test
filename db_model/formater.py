from datetime import date


def date_format(date_str):
    """ Форматируем дату из формата ММ/ДД/ГГГГ в ГГГГ-ДД-ММ """
    
    if len(date_str) != 10:
        return date.today()

    date_list = date_str.split('/')
    return '{}-{}-{}'.format(date_list[2], date_list[0], date_list[1])


def stock_prices(company, arg_list: list):
    return {
        'company': company,
        'date': date_format(arg_list[0]),
        'open': arg_list[1],
        'high': arg_list[2],
        'low': arg_list[3],
        'close': arg_list[4],
        'volume': arg_list[5].replace(',', '')
    }


def insiders(company, arg_list: list):
    return {
        'company': company,
        'name': arg_list[0],
        'relation': arg_list[1]
    }


def trades(insider, arg_list: list):
    return {
        'insider': insider,
        'date': date_format(arg_list[2]),
        'type': arg_list[3],
        'owner_type': arg_list[4],
        'traded': arg_list[5].replace(',', ''),
        'price': arg_list[6],
        'held': arg_list[7].replace(',', '')
    }
