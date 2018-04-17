#!/bin/python

import bs4
import requests
import json
from time import sleep
from datetime import datetime


root = 'https://www.liquipedia.net/smash/'
sub = 'List of national tournaments'


def get_wiki_section(root, page, section):
    r = requests.get("{0}/{1}".format(root, page),
                     headers={"Accept-Encoding": "gzip",
                              "User-Agent": "variatrix/1.0 (https://sashahashi.github.io; sasham@fastmail.com)"})
    sleep(1)
    soup = bs4.BeautifulSoup(r.text, 'lxml')

    content = soup.select("#mw-content-text > table > tr > td")[0]

    section_start = content.find_all("span", id=section)[0].find_parent()

    if section_start:
        for tag in section_start.find_previous_siblings():
            if isinstance(tag, bs4.Tag):
                tag.decompose()

        section_end = section_start.find_next("h2")

        for tag in section_end.find_next_siblings():
            if isinstance(tag, bs4.Tag):
                tag.decompose()
        section_end.decompose()

        return content


# def get_results(name):

def parse_date(days, year):
    if "-" in days:
        start, end = days.split("-")
    else:
        start, end = days, days

    start, end = start.strip(), end.strip()

    start_month, start_day = start.split(" ")
    if " " in end:
        end_month, end_day = end.split(" ")
    else:
        end_month, end_day = start_month, end

    start_day = start_day.rstrip('st nd rd th')
    end_day = end_day.rstrip('st nd rd th')

    start_date = datetime.strptime("{0} {1} {2}".format(start_month, start_day, year), "%B %d %Y")
    end_date = datetime.strptime("{0} {1} {2}".format(end_month, end_day, year), "%B %d %Y")

    return (start_date, end_date)


def __main__():
    content = get_wiki_section(root, sub, "Super_Smash_Bros._Melee")

    year = 2003
    for table in content.find_all('table'):
        for tr in table.find_all('tr'):
            if tr.find_all('td'):
                name, date, entrants, winner = tr.find_all('td')
                href = name.a['href']
                name = name.a.string

                start_date, end_date = parse_date(date.string, year)
                print(name, start_date, end_date, sep="\t")
        year += 1


if __name__ == "__main__":
    __main__()
