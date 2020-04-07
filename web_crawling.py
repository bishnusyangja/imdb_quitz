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

    def fetch_winner_urls(self, url):
        print('fetching winner urls .....')
        resp = requests.get(f'{self.ROOT_URL}{url}')
        bs = BeautifulSoup(resp.text, 'html.parser')
        anc = bs.find('a', attrs={'title': 'Winners'})
        if hasattr(anc, 'attrs'):
            winners_url = anc.attrs.get('href')
            print('found winners url.... ', winners_url)
        else:
            winners_url = ''
        return winners_url

    def fetch_winner_content(self, url):
        print('fetching winner content .....')
        url = f'{self.ROOT_URL}{url}'
        resp = requests.get(url)
        bs = BeautifulSoup(resp.text, 'html.parser')
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

    def extract_content_from_data(self, data):
        data_list = []
        awards = data['nomineesWidgetModel']['eventEditionSummary']['awards']
        for award in awards:
            award_name = award['awardName']
            if award_name in ('Oscar', 'Primetime Emmy'):
                for category in award['categories']:
                    category_name = category['categoryName']
                    data_dict = {'award': award_name, 'category': category_name}
                    choices = []
                    winner = ''
                    for nominees in category['nominations']:
                        try:
                            item = nominees['primaryNominees'][0]['name']
                        except Exception as exc:
                            print(exc)
                        else:
                            is_winner = nominees['isWinner']
                            if is_winner:
                                winner = item
                            choices.append(item)
                    data_dict['choices'] = choices
                    data_dict['winner'] = winner
                    data_list.append(data_dict)
        return data_list


def data_for_oscar_award(obj, oscar_url):
    winners_url = obj.fetch_winner_urls(oscar_url)
    oscar_data = obj.fetch_winner_content(winners_url)
    return obj.extract_content_from_data(oscar_data)


def data_for_emmys_award(obj, emmys_url):
    winners_url = obj.fetch_winner_urls(emmys_url)
    emmys_data = obj.fetch_winner_content(winners_url)
    return obj.extract_content_from_data(emmys_data)


def crawl_imdb_content():
    obj = WebScrapping()
    oscar_url, emmys_url = obj.fetch_oscar_emmy_url()
    oscar_data = data_for_oscar_award(obj, oscar_url)
    emmys_data = data_for_emmys_award(obj, emmys_url)
    print(oscar_data[:10])
    print(emmys_data[:10])


crawl_imdb_content()
