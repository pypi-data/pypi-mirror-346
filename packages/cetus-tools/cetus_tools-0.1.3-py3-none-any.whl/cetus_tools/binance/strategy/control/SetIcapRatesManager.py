import requests
import time

class SetIcapRatesManager:
    def __init__(self, url):
        self.url = url
    
    def getSetIcapRate(self, prices):
        items = (requests.get(self.url + '/v1/rates?source=CMA&symbol=USDCOP').json())['payload']
        if not self.isNull(items[0]):
            return self.parseSetIcapRate(items[0], prices)
        return None if self.isNull(items[1]) else self.parseSetIcapRate(items[1], prices)
    
    def isNull(self, item):
        return ('bid' in item.keys()) and ('ask' in item.keys()) and item['bid'] == '-' and item['ask'] == '-'
    
    def parseSetIcapRate(self, datum, prices):
        result = {
            'timestamp': 1000 * time.time(),
            'ask': float(datum['ask']) if datum['ask'] != '-' else 0,
            'bid': float(datum['bid']) if datum['bid'] != '-' else 0
        }
        for price in prices:
            result[price['name']] = max(result[price['key']] - price['spread'], 0)
        return result