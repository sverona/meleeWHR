#!/usr/bin/python

from bs4 import BeautifulSoup
import json
import requests as r
from time import sleep
import os


def get_brackets(url):
    headers = {"Accept-Encoding": "gzip",
               "User-Agent": "variatrix/1.0 (https://sashahashi.github.io; sasham@fastmail.com)"}
    html = r.get(url, headers=headers).text
    soup = BeautifulSoup(html, 'lxml')
    for tag in soup.select("div.tabs-static-games"):
        tag.decompose()

    for tag in soup.select("div.tabs-static"):
        for a in tag.find_all('a'):
            if a['title']:
                bracket_soup_url = 'http://liquipedia.net/smash/index.php?title={0}&action=edit'.format(a['title'])
                print(bracket_soup_url)
                bracket_soup_html = r.get(bracket_soup_url, headers=headers).text
                bracket_soup = BeautifulSoup(bracket_soup_html, 'lxml')

                for bracket in bracket_soup.select("textarea#wpTextbox1"):
                    dirname, filename = a['title'].rsplit('/', 1)
                    if not os.path.isdir(dirname):
                        os.makedirs(dirname)
                    with open(a['title'] + '.wiki', 'w') as f:
                        f.write(bracket.string)
            sleep(5)


def __main__():
    with open('cache.txt', mode='r+') as cache:
        parsed = cache.read().split('\n')
        print(parsed)

        tournaments = json.load(open('all_tournaments.json'))
        for name, data in tournaments.items():
            if name not in parsed:
                print(name)
                get_brackets(data['fullurl'])
                cache.write("\n")
                cache.write(name)

                sleep(5)


if __name__ == '__main__':
    __main__()
