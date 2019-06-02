import time
import argparse
import threading
import urllib.request

from queue import Queue, Empty
from bs4 import BeautifulSoup

from db_model import base, formater


HISTORY_URL = 'https://www.nasdaq.com/symbol/{}/historical'
TRADE_URL = 'https://www.nasdaq.com/symbol/{}/insider-trades?page={}'
LIMIT_PAGE = 10
START_PAGE = 1
SLEEP_SEC = 0.01
MAX_ERR_COUNT = 500


def create_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('-n', type=int, default=2)
    parser.add_argument('-f', '--file', type=str, default='tickers.txt')

    return parser


def history_fill(service):
    service = service.decode()
    bs = BeautifulSoup(urllib.request.urlopen(HISTORY_URL.format(service)).read(), 'html.parser')
    table = bs.find(id='quotes_content_left_pnlAJAX').table
    if table is None:
        return

    tbody = table.tbody.find_all('tr')
    tbody.pop(0)

    for tr in tbody:
        str_list = []
        for td in tr.find_all('td'):
            str_list.append(td.get_text().strip())

        base.StockPricesModel(**formater.stock_prices(service, str_list)).save()


def trade_fill_page(service, page):
    service = service.decode()
    bs = BeautifulSoup(urllib.request.urlopen(TRADE_URL.format(service, page)).read(), 'html.parser')

    tbody = bs.find('div', {'class': 'genTable'}).table.find_all('tr')
    tbody.pop(0)

    for tr in tbody:
        str_list = []
        for td in tr.find_all('td'):
            if td.a is None:
                str_list.append(td.get_text().strip())
            else:
                str_list.append(td.a.get_text().strip())

        insider_data = formater.insiders(service, str_list)

        with data_lock:
            insider = base.InsidersModel.get_or_none(
                *(base.InsidersModel.company == service, base.InsidersModel.name == insider_data['name'])
            )
            if insider is None:
                insider = base.InsidersModel(**insider_data)
                insider.save()

        base.TradesModel(**formater.trades(insider, str_list)).save()


def trade_fill(service):
    bs = BeautifulSoup(urllib.request.urlopen(TRADE_URL.format(service.decode(), START_PAGE)).read(), 'html.parser')

    pages = bs.find(id='pagerContainer')
    if pages is None:
        return

    for link in pages.find_all('a'):
        try:
            page = int(link.get_text())
            if page < LIMIT_PAGE:
                max_page = page
            else:
                max_page = LIMIT_PAGE
                break
        except ValueError:
            pass

    with lock:
        for current_page in range(max_page):
            queue.put({'args': (service, current_page), 'method': trade_fill_page})


def delete_data(service):
    insider = base.InsidersModel.delete().where(base.InsidersModel.company == service)
    insider.execute()
    stock_price = base.StockPricesModel.delete().where(base.StockPricesModel.company == service)
    stock_price.execute()


class ParserThread(threading.Thread):

    def __init__(self, queue, lock):
        super().__init__()
        self.queue = queue
        self.lock = lock
        self.running = True
        self.err_count = 0

    def run(self):
        print('Thread %s start' % (self.name,))
        while self.running:
            with self.lock:
                try:
                    quest = self.queue.get_nowait()
                    self.err_count = 0
                except Empty:
                    # При (MAX_ERR_COUNT / 100) секундах бездействия, умираем
                    if self.err_count == MAX_ERR_COUNT:
                        self.running = False
                    self.err_count += 1
                    time.sleep(SLEEP_SEC)
                    continue
            print('Thread %s start request: %r' % (self.name, quest))
            quest['method'](*quest['args'])
            print('Thread %s end request' % (self.name,))
        print('Thread %s stop' % (self.name,))


if __name__ == '__main__':
    parser = create_parser()
    arguments = parser.parse_args()
    lock = threading.Lock()
    data_lock = threading.Lock()
    queue = Queue()
    workers = []

    with open(arguments.file, 'r') as f:
        for company in f:
            company = company.strip().lower().encode()
            delete_data(company)
            queue.put({'args': (company,), 'method': history_fill})
            queue.put({'args': (company,), 'method': trade_fill})

    arguments.n = arguments.n if arguments.n > 0 else 1

    for _ in range(arguments.n):
        worker = ParserThread(queue, lock)
        worker.start()
        workers.append(worker)

    for worker in workers:
        worker.join()
