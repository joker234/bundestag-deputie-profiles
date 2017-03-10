#!/usr/bin/env python3

import string
import requests
from bs4 import BeautifulSoup
import lxml
from urllib.parse import urljoin
import re
import pprint

result = []

for c in string.ascii_uppercase:
    # this works if there are only up to 120 deputies per first character (last_name)
    for offset in range(0, 101, 20):
        url = "https://www.bundestag.de/ajax/filterlist/de/abgeordnete18/-/440460/h_3b8326811f14c63004d3675a926daac6?limit=20&offset={}&noFilterSet=false&prsnNachname=440448%23{}*".format(offset, c)
        # For debugging purposes
        # print("{}, {}".format(c, offset))
        # or
        # print("{}, {}:     {}".format(c, offset, url))

        r = requests.get(url)
        r.encoding = 'UTF-8'

        soup = BeautifulSoup(r.text, 'lxml')

        deputies = soup.find_all('div', class_="bt-slide-content")
        for deputy in deputies:
            res_d = {}
            a = deputy.find('a', class_="bt-open-in-overlay")
            party = a.find('p', class_="bt-person-fraktion")
            res_d['last_name'], res_d['first_name'] = a['title'].split(", ")
            res_d['bundestag_url'] = urljoin(url, a['href'])
            res_d['party'] = re.sub(r'^\s+', '', party.text)
            result.append(res_d)

# do whatever you want with the list result
pprint.pprint(result)
