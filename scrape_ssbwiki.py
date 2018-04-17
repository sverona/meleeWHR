#!/bin/python

from bs4 import BeautifulSoup
import requests
from time import sleep


class Scraper:

    def __init__(self, root, max_depth):
        self.root = root
        self.max_depth = max_depth
        self.visited = set()

    def scrape(self, root):
        return self._scrape(root, 0)

    def _scrape(self, page, depth):
        if page not in self.visited:
            yield (depth, page)
            self.visited.add(page)
            sleep(1.5)

        if depth <= self.max_depth:
            html = requests.get(page).text
            soup = BeautifulSoup(html, 'lxml')
            content = soup.find('div', id='mw-content-text')

            article_icons = soup.find('div', id="ArticleIcons")
            if article_icons:
                article_icons.decompose()

            edits = soup.find_all('span', class_='mw-editsection')
            for edit in edits:
                edit.decompose()

            for link in content.find_all("a"):
                try:
                    skips = ["#", "/Super", "/Special:", "/File:", "http"]
                    if not any(link["href"].startswith(x) for x in skips):
                        for outpage in self._scrape(self.root + link["href"].strip("/"), depth + 1):
                            yield outpage
                except KeyError:
                    pass


nodes = {}

root = 'https://www.ssbwiki.com/'
sub = 'SoCal_Melee_Power_Rankings'

s = Scraper(root, 5)

for page in s.scrape(root + sub):
    print('\t' * page[0], page[1], flush=True)
