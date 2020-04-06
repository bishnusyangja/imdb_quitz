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

    def fetch_oscar_content(self, url):
        print('fetching oscar content.....')
        resp = requests.get(f'{self.ROOT_URL}{url}')
        bs = BeautifulSoup(resp.text, 'html.parser')
        anc = bs.find('a', attrs={'title': 'Winners'})
        if hasattr(anc, 'attrs'):
            winners_url = anc.attrs.get('href')
            print('found winners url.... ', winners_url)
        else:
            winners_url = ''
        return winners_url

    def fetch_oscar_winner_urls(self, url):
        print('fetching oscar winners.....')
        resp = requests.get(f'{self.ROOT_URL}{url}')
        bs = BeautifulSoup(resp.text, 'html.parser')

        for year_div in bs.find_all('div', attrs={'class': 'event-history-widget__years-row'}):
            print(year_div)
            anc = year_div.find('a')
            print(anc.get_text(), anc.attrs.get('href'))


def crawl_imdb_content():
    obj = WebScrapping()
    oscar_url, emmys_url = obj.fetch_oscar_emmy_url()
    winners_url = obj.fetch_oscar_content(oscar_url)
    obj.fetch_oscar_winner_urls(winners_url)
    # print(winners_url)
    # print(oscar_url, emmys_url)




crawl_imdb_content()