import queue
import re
import requests
import socket
import sys
import time
from bs4 import BeautifulSoup

import config
import util

BASE_URL = 'https://www.booking.com/'

def search(location):
    query = {
        'rows': config.RESULT_COUNT,
        'ss': location,
        'checkin_month': config.CHECK_IN.month,
        'checkin_monthday': config.CHECK_IN.day,
        'checkin_year': config.CHECK_IN.year,
        'checkout_month': config.CHECK_OUT.month,
        'checkout_monthday': config.CHECK_OUT.day,
        'checkout_year': config.CHECK_OUT.year,
        'no_rooms': config.ROOM_COUNT,
        'group_adults': config.ADULT_COUNT,
        'group_children': config.CHILD_COUNT,
    }
    session = requests.Session()
    session.headers = config.HEADERS
    session.get(BASE_URL)
    response = session.get(BASE_URL + 'searchresults.en-us.html', params=query)
    soup = BeautifulSoup(response.text, 'lxml')
    return soup.find_all('div', class_='sr_item')

def parse_result(result):
    hotel = -1
    price = -1
    hotel_attr = result.get('data-hotelid')
    price_tag = (
        result.find('div', class_='bui-price-display__value')
        or result.find('strong', class_='price')
    )
    if hotel_attr:
        hotel = int(hotel_attr)
    if price_tag:
        price_group = re.search('[\d,]+', price_tag.text).group(0)
        price = int(price_group.replace(',', ''))
    return hotel, price

def scrape(queue, location_code, rate):
    utc = time.gmtime()
    location_curr = socket.gethostname()
    results = search(config.LOCATION[location_code])
    for index, result in enumerate(results):
        hotel, price_local = parse_result(result)
        price = util.usd(price_local, config.CURRENCY[location_curr], rate)
        queue.put(['book', location_curr, location_code, index,
            hotel, price_local, price, utc.tm_yday, utc.tm_hour])

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
