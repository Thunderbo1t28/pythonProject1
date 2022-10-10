import requests
from logging import getLogger

logger = getLogger(__name__)





class BinanceP2P(object):
    def __int__(self):
        self.base_url ="https://p2p.binance.com/bapi/c2c/v2/friendly/c2c/adv/search"

    def __request(self):
        url = "https://p2p.binance.com/bapi/c2c/v2/friendly/c2c/adv/search"
        headers = {'method': 'post', 'contentType': 'application/json'}
        data = {"page": 1,
                "rows": 1,
                "payTypes": ["TinkoffNew"],
                "asset": "USDT",
                "tradeType": "BUY",
                "fiat": "RUB",
                "merchantCheck": True}
        #print(url)


        r = requests.post(url=url, headers=headers, json=data)
        resultRUB = r.json()
        kursRUB = float(resultRUB["data"][0]["adv"]["price"])


        dataKZT = {"page": 1,
                   "rows": 1,
                   "payTypes": ["KaspiBank"],
                   "asset": "USDT",
                   "tradeType": "SELL",
                   "fiat": "KZT",
                   "merchantCheck": True}
        rKZT = requests.post(url=url, headers=headers, json=dataKZT)
        resultKZT = rKZT.json()
        kursKZT = float(resultKZT["data"][0]["adv"]["price"])
        #(((kursKZT / kursRUB) / 100) * 3) +
        result = (kursKZT / kursRUB)
        return round(result,2)

    def get_data(self):

        return self.__request()
