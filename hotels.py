import queue
import re
import requests
import socket
import sys
import time
from bs4 import BeautifulSoup

import config
import util

BASE_URL = 'https://www.hotels.com/'
PAGES = 3

def descend(dictionary, levels):
    level, *levels = levels
    prev_level = dictionary.get(level)
    for level in levels:
        if prev_level:
            prev_level = prev_level.get(level)
    return prev_level

def search(location, page_number):
    query = {
        'pn': page_number,
        'q-destination': location,
        'q-localised-check-in': config.CHECK_IN.strftime('%m/%d/%y'),
        'q-localised-check-out': config.CHECK_OUT.strftime('%m/%d/%y'),
        'q-rooms': config.ROOM_COUNT,
        'q-room-0-adults': config.ADULT_COUNT,
        'q-room-0-children': config.CHILD_COUNT,
    }
    session = requests.Session()
    session.headers = config.HEADERS
    session.get(BASE_URL)
    response = session.get(BASE_URL + 'search/listings.json', params=query)
    try:
        json = response.json()
    except ValueError:
        json = {}
    results = descend(json, ['data', 'body', 'searchResults', 'results'])
    if not results:
        results = []
    return results

def parse_result(result):
    hotel = -1
    price = -1
    hotel_attr = result.get('id')
    price_string = descend(result, ['ratePlan', 'price', 'current'])
    if hotel_attr:
        hotel = hotel_attr
    if price_string:
        price_group = re.search('[\d,]+', price_string).group(0)
        price = int(price_group.replace(',', ''))
    return hotel, price

def scrape(queue, location_code, rate):
    utc = time.gmtime()
    location = config.LOCATION[location_code]
    location_curr = socket.gethostname()
    results = [x for i in range(PAGES) for x in search(location, i)]
    for index, result in enumerate(results):
        hotel, price_local = parse_result(result)
        price = util.usd(price_local, config.CURRENCY[location_curr], rate)
        queue.put(['hot', location_curr, location_code, index,
            hotel, price, utc.tm_yday, utc.tm_hour])

def main(argv):
    rate = {
        'EUR': 1,
        'USD': 1.116931,
        'CAD': 1.506685,
        'GBP': 0.882129,
        'INR': 78.05954,
        'SGD': 1.540751,
    }
    que = queue.Queue()
    scrape(que, argv[1], rate)
    while not que.empty():
        print(que.get())

if __name__ == '__main__':
    main(sys.argv)
