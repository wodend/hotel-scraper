import queue
import re
import requests
import socket
import sys
import time
from bs4 import BeautifulSoup

import config

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

def scrape(queue, location_code):
    utc = time.gmtime()
    location = config.LOCATION[location_code]
    results = [x for i in range(PAGES) for x in search(location, i)]
    for index, result in enumerate(results):
        hotel, price = parse_result(result)
        queue.put(['hot', socket.gethostname(), location_code, index,
            hotel, price, utc.tm_yday, utc.tm_hour])

def main(argv):
    que = queue.Queue()
    scrape(que, argv[1])
    while not que.empty():
        print(que.get())

if __name__ == '__main__':
    main(sys.argv)
