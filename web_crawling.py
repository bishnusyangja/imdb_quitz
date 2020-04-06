import json
import re

import requests
from bs4 import BeautifulSoup

ROOT_URL = 'https://imdb.com'


class WebScrapping:
    ROOT_URL = 'https://imdb.com'

    def fetch_oscar_emmy_url(self):
        url = self.ROOT_URL
        print('fetching base response.....')
        resp = requests.get(url)
        bs = BeautifulSoup(resp.text, 'html.parser')
        oscar_url, emmys_url = None, None
        for anc in bs.find_all('a', attrs={'role': 'menuitem'}):
            span = anc.find('span')
            if span and span.get_text().strip().lower() == 'oscars':
                oscar_url = anc.attrs.get('href')
                print('found oscar url : ', oscar_url)
            if span and span.get_text().strip().lower() == 'emmys':
                emmys_url = anc.attrs.get('href')
                print('found emmys url : ', emmys_url)
            if oscar_url and emmys_url:
                break
        return oscar_url, emmys_url

    def fetch_oscar_winner_urls(self, url):
        print('fetching oscar winner urls .....')
        resp = requests.get(f'{self.ROOT_URL}{url}')
        bs = BeautifulSoup(resp.text, 'html.parser')
        anc = bs.find('a', attrs={'title': 'Winners'})
        if hasattr(anc, 'attrs'):
            winners_url = anc.attrs.get('href')
            print('found winners url.... ', winners_url)
        else:
            winners_url = ''
        return winners_url

    def fetch_oscar_winner_content(self, url):
        print('fetching oscar winners.....')
        url = f'{self.ROOT_URL}{url}'
        print('oscar nominies url ', url)
        resp = requests.get(url)
        bs = BeautifulSoup(resp.text, 'lxml')

        js_scripts = bs.find_all('script')

        for i_script in js_scripts:
            check_string = 'IMDbReactWidgets.NomineesWidget.push'
            text = i_script.get_text()
            if check_string in text:
                first_string = """{"nomineesWidgetModel":"""
                second_string = "}]);"
                try:
                    first_idx = text.index(first_string)
                    second_idx = text.index(second_string)
                    content = text[first_idx: second_idx+1]
                    return json.loads(content)
                except Exception as exc:
                    print("Exception", exc)
        return {}

    def extract_content_from_raw_data(self, data):
        awards = data['nomineesWidgetModel']['eventEditionSummary']['awards']
        for award in awards:
            award_name = award['awardName']
            print('************\n')
            if award_name in ('oscar', 'Primetime Emmy'):
                for category in award['categories']:
                    category_name = category['categoryName']
                    print('.........')
                    for nominees in category['nominations']:
                        item = nominees['primaryNominees'][0]['name']
                        is_winner = nominees['isWinner']
                        print(award_name, category_name, item, is_winner)

    def fetch_emmys_winner_urls(self, url):
        print('fetching oscar winner urls .....')
        resp = requests.get(f'{self.ROOT_URL}{url}')
        bs = BeautifulSoup(resp.text, 'html.parser')
        anc = bs.find('a', attrs={'title': 'Winners'})
        if hasattr(anc, 'attrs'):
            winners_url = anc.attrs.get('href')
            print('found winners url.... ', winners_url)
        else:
            winners_url = ''
        return winners_url

    def fetch_emmys_winner_content(self, url):
        print('fetching emmys winners.....')
        url = f'{self.ROOT_URL}{url}'
        print('emmys nominies url ', url)
        resp = requests.get(url)
        bs = BeautifulSoup(resp.text, 'lxml')

        js_scripts = bs.find_all('script')

        for i_script in js_scripts:
            check_string = 'IMDbReactWidgets.NomineesWidget.push'
            text = i_script.get_text()
            if check_string in text:
                first_string = """{"nomineesWidgetModel":"""
                second_string = "}]);"
                try:
                    first_idx = text.index(first_string)
                    second_idx = text.index(second_string)
                    content = text[first_idx: second_idx+1]
                    return json.loads(content)
                except Exception as exc:
                    print("Exception", exc)
        return {}



def data_for_oscar_award(obj, oscar_url):
    winners_url = obj.fetch_oscar_winner_urls(oscar_url)
    winners_url = '/oscars/nominations/'
    oscar_data = obj.fetch_oscar_winner_content(winners_url)
    obj.extract_oscar_content(oscar_data)


def data_for_emmys_award(obj, emmys_url):
    # winners_url = obj.fetch_emmys_winner_urls(emmys_url)
    winners_url = '/emmys/nominations/'
    emmys_data = obj.fetch_emmys_winner_content(winners_url)
    obj.extract_oscar_content(emmys_data)
    print(winners_url)


def crawl_imdb_content():
    obj = WebScrapping()
    oscar_url, emmys_url = obj.fetch_oscar_emmy_url()
    # data_for_oscar_award(obj, oscar_url)
    data_for_emmys_award(obj, emmys_url)

    # print('winners url ', winners_url)
    # print(oscar_url, emmys_url)




crawl_imdb_content()