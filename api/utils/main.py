
# get popular web-series in netflix 

import requests, json
from bs4 import BeautifulSoup

from collections import defaultdict
class NetflixDataScraper():
    def __init__(self, url="https://www.netflix.com/in/browse/genre/1191605") -> None:
        self.url = url
        self.section_class = 'nm-collections-row'
        self.list_class = 'nm-content-horizontal-row-item'
        self.span_class = 'nm-collections-title-name'
        self.categories = []
        self.soup = self._soup()
        self.data = defaultdict(list)

    def _soup(self):
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
        r = requests.get(self.url, headers=headers)
        return BeautifulSoup(r.content, 'html5lib')

    def sections(self) -> list:
        return self.soup.find_all('section', {'class': self.section_class})

    @classmethod
    def category(cls, section=None) -> str:
        if section:
            return section.h2.text[:-12] if 'Explore more' in section.h2.text else section.h2.text
    
    def _shows_items(self,section=None) -> list:
        if section:
            return section.find_all('li', {'class': self.list_class})

    def get_data(self) -> None:
        for section in self.sections():
            _cat_list = self.category(section)
            shows = [
                {
                    "name": item.a.find('span', self.span_class).text,
                    "url": item.a['href']
                }
                for item in self._shows_items(section=section) if item.a
                ]
            self.data[_cat_list] = shows

if __name__ == "__main__":
    nt = NetflixDataScraper()
    nt.get_data()
    print(nt.data)
