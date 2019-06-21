import requests
from html_to_etree import parse_html_bytes
import os

class CategoryFetcher:

    def __init__(self):
        self.base_url = 'http://weapon.huanqiu.com/'
        self.file_path = './category.txt'

    def _start_request(self):
        self._parse_big_category(self.base_url)

    def _parse_big_category(self, url):
        tree = self._request_html(url)
        big_category_lt = tree.xpath('//div[@class="sideNav"]//li/a/text()')
        print(big_category_lt)
        big_category_url_lt = tree.xpath('//div[@class="sideNav"]//li/a/@href')
        dt = dict()
        for name, url in zip(big_category_lt, big_category_url_lt):
            dt[name] = set(self._parse_small_category(self.base_url + url))

        self._save_data(dt)


    def _parse_small_category(self, url):
        tree = self._request_html(url)
        return tree.xpath('//div[@class="select"]/ul[1]/li/span[@class="list"]/a/text()')

    def _request_html(self, url):
        html = requests.get(url).content
        print(html)
        return parse_html_bytes(html)

    def _save_data(self, dt):
        if os.path.exists(self.file_path):
            os.remove(self.file_path)
        with open(self.file_path, 'w', encoding='utf8') as file:
            file.write(repr(dt))


if __name__ == '__main__':
    CategoryFetcher()._start_request()