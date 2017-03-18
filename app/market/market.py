# market.py

import requests
import re
from . import market_mod
from app.utils.evedb.evedb import EveDb
from BeautifulSoup import BeautifulStoneSoup

EVECENTRAL = "http://api.eve-central.com/api/marketstat?typeid=%s&minQ=1&&regionlimit=10000002"
evedb = EveDb()


@market_mod.register_cmd(r'^!getprice')
def getprice(data):
    if evedb.conn:
        cmd = data['text'].split()

        if len(cmd) > 1:
            item_name, formattedprice, _ = itemtoprice(" ".join(cmd[1:]))
            return "{}: {} ISK".format(item_name, formattedprice)
        else:
            return "Usage: `!getprice item`"
    else:
        return "EVE static data dump not loaded"


def itemtoprice(item):
    try:
        item_name, item_id = evedb.get_type_id(item)
        url = EVECENTRAL % item_id
        soup = BeautifulStoneSoup(requests.get(url).text)
        price = str(soup.find("sell").min)
        removetags = re.compile("<(.|\n)*?>")
        price = removetags.sub("", price)
        price = float(price)
        if price == 0:
            raise ZeroDivisionError
        import locale
        locale.setlocale(locale.LC_ALL, "")
        if price < 1e6:
            formattedprice = locale.format('%.2f', price, True)
        else:
            formattedprice = locale.format('%d', price, True)
        return item_name, formattedprice, price
    except Exception:
        return None, None, None
