import requests
from pprint import pprint
import json
from pathlib import Path
import time


class Products:

    def __init__(self, start_url):
        self.url = start_url

    def get_response(self, url, **kwargs):
        while True:
            try:
                response = requests.get(url, **kwargs)
                if response.status_code != 200:
                    raise Exception
                time.sleep(0.05)
                return response
            except Exception:
                time.sleep(0.25)

    def parse(self, url, **kwargs):
        while url:
            response = self.get_response(url, **kwargs)
            data = response.json()
            url = data['next']
            for product in data['results']:
                yield product

    def save(self, data: dict, file_path):
        with open(file_path, 'w', encoding='UTF-8') as file:
            json.dump(data, file, ensure_ascii=False)


class Parser5ka(Products):

    def __init__(self, start_url, url_catalog):
        self.url_catalog = url_catalog
        super().__init__(start_url)

    def start(self):
        params = {}
        for category in (self.get_response(self.url_catalog, headers=HEADER)).json():
            categoty_dict = {}
            products_list = []
            categoty_dict['name'] = category['parent_group_name']
            categoty_dict['code'] = category['parent_group_code']
            params['categories'] = category['parent_group_code']

            for product in self.parse(self.url, headers=HEADER, params=params):
                products_list.append(product)

            if products_list:
                categoty_dict['products'] = products_list
                file_path = Path(__file__).parent.joinpath('products', f'{categoty_dict["name"]}.json')
                self.save(categoty_dict, file_path)




if __name__ == '__main__':
    HEADER = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 YaBrowser/20.11.3.183 Yowser/2.5 Safari/537.36'}

    URL= 'https://5ka.ru/api/v2/special_offers/'
    URL_CATEGORY = 'https://5ka.ru/api/v2/categories/'

    d = Parser5ka(URL, URL_CATEGORY)
    d.start()



