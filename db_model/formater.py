from datetime import date


def stock_prices(company, arg_list: list):
    if len(arg_list[0]) != 10:
        row_date = date.today()
    else:
        date_list = arg_list[0].split('/')
        row_date = '{}-{}-{}'.format(date_list[2], date_list[0], date_list[1])

    return {
        'company': company,
        'date': row_date,
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
    if len(arg_list[2]) != 10:
        row_date = date.today()
    else:
        date_list = arg_list[2].split('/')
        row_date = '{}-{}-{}'.format(date_list[2], date_list[0], date_list[1])

    return {
        'insider': insider,
        'date': row_date,
        'type': arg_list[3],
        'owner_type': arg_list[4],
        'traded': arg_list[5].replace(',', ''),
        'price': arg_list[6],
        'held': arg_list[7].replace(',', '')
    }
