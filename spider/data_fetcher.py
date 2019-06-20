from bs4 import BeautifulSoup
import requests
import os
import sys
import re


class DataFetcher:

    def __init__(self):
        self.base_url = "http://weapon.huanqiu.com/"
        self.save_path = "./data.txt"
        if os.path.exists(self.save_path):
            os.remove(self.save_path)

    def start_request(self):
        weapon_page = requests.get(self.base_url + 'weaponlist').content
        bs = BeautifulSoup(weapon_page, "lxml")
        for cls_link in bs.select('.sideNav li a'):
            cls_url = self.base_url + cls_link.get('href')
            print(cls_url)
            # try:
            self.parse_list(cls_url)
            # except Exception as e:
            #     self.dump_exception(repr(e))
            # break

    def parse_list(self, url):
        page_content = requests.get(url).content
        bs = BeautifulSoup(page_content, "lxml")
        items = bs.select(".picList li")
        if not items or not len(items):
            print(items)
            return
        for item in items:
            pic_container = item.select_one('span.pic')
            detail_url = self.base_url + pic_container.select_one('a').get('href')
            print(detail_url)
            model = dict()
            # model['img_url'] = self.base_url + pic_container.select_one('a img').get('src')
            model['desc'] = pic_container.get_text()
            model['name'] = item.select_one('span.name a').get_text()
            model['country'] = item.select_one('div.country a b').get_text()
            category_period = item.select_one('span.category').get_text()
            model['category'] = category_period.split('|')[0].strip()
            model['period'] = category_period.split('|')[1].strip()
            self.parse_detail(detail_url, model)
            # break
            # time.sleep(0.5)

        re_resutlt = re.findall('\S+_(\d+)', url)
        next_page = 2
        if re_resutlt:
            next_page = int(re_resutlt[0]) + 1

        print(url)
        page_suffix = re.findall('\S+(\/list_\S+)', url)
        if page_suffix:
            url = url.replace(page_suffix[0], '')
        next_page_url = url + '/list_0_0_0_0_{}'.format(next_page)
        print('next_page_url', next_page_url)
        self.parse_list(next_page_url)


    def parse_detail(self, detail_url, model):
        try:
            if model is None or not isinstance(model, dict):
                model = {}
            html = requests.get(detail_url).content
            bs = BeautifulSoup(html, "lxml")

            con_main = bs.select_one('div.detail  div.conMain')
            model['intro'] = con_main.select_one('div.intron').get_text().strip()
            for other_item in con_main.select('div.otherList'):
                other_title = other_item.select_one('h3').get_text().strip()
                other_intro = other_item.select_one('div').get_text().strip()
                model[other_title] = other_intro

            con_side = bs.select_one('div.detail div.side')
            for side_item in con_side.select('ul.dataList li'):
                attr = side_item.get_text().strip().replace('"', '').split('：', 1)
                model[attr[0]] = attr[1]

            for title, side_item in zip(con_side.select('h4'), con_side.select('ul.multiList')):
                model[title.get_text().strip()] = side_item.get_text().strip()
        except Exception as e:
            self.dump_exception(repr(e))

        self.save_data(model)

    def save_data(self, model):
        print(model)
        with open(self.save_path, 'a+', encoding='utf8') as file:
            file.write(str(model))
            file.write('\n')

    @staticmethod
    def dump_exception(e):
        with open('./exception.txt', 'a+', encoding='utf8') as file:
            file.write(e)
            file.write('\n')


if __name__ == "__main__":
    sys.setrecursionlimit(100000)
    data_fetcher = DataFetcher()
    data_fetcher.start_request()
    # url = "http://weapon.huanqiu.com//weaponlist/aircraft/list_0_0_0_0_12"
    # print(re.findall('\S+_(\d+)', url))
    # re.sub('\S+(\/list_\S+)', '', url)
    # print(url)
    # print(re.findall('\S+(\/list_\S+)',  url))
    # print(url.replace(re.findall('\S+(\/list_\S+)',  url)[0], ''))
    # data_fetcher.parse_detail('http://weapon.huanqiu.com//m70', None)
