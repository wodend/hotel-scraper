import queue
import requests
import sys

import config

BASE_URL = "https://{0}.agoda.com/"
DEFAULT_TIME = 'T00:00:00'
LOCATION = {
    'ny': 318,
    'sf': 13801,
    'london': 233,
    'frankfurt': 15847,
    'amster': 13868,
    'bangal': 4923,
    'singap': 4064,
    'toronto': 17052,
}

def search(location):
    stay_length = config.CHECK_OUT.day - config.CHECK_IN.day
    query = {
        'SearchType': 1,
        'PageSize': config.RESULT_COUNT,
        'CityId': location,
        'CheckIn': str(config.CHECK_IN) + DEFAULT_TIME,
        'CheckOut': str(config.CHECK_OUT) + DEFAULT_TIME,
        'LengthOfStay': stay_length,
        'Adults': config.ADULT_COUNT,
        'Children': config.CHILD_COUNT,
        'Rooms': config.ROOM_COUNT,
    }
    session = requests.Session()
    session.headers = config.HEADERS
    session.get(BASE_URL.format('www'))
    response = session.post(
        BASE_URL.format('ash') + 'api/en-us/Main/GetSearchResultList',
        json=query,
    )
    try:
        json = response.json()
    except ValueError:
        json = {}
    return json.get('ResultList')

def parse_result(result):
    hotel = -1
    price = -1
    hotel_attr = result.get('HotelID')
    price_string = result.get('FormattedDisplayPrice')
    if hotel_attr:
        hotel = hotel_attr
    if price_string:
        price = int(price_string)
    return hotel, price

def scrape(queue, location_code):
    results = search(LOCATION[location_code])
    for index, result in enumerate(results):
        hotel, price = parse_result(result)
        queue.put(['agoda', location_code, index, hotel, price])

def main(argv):
    que = queue.Queue()
    scrape(que, argv[1])
    while not que.empty():
        print(que.get())

if __name__ == '__main__':
    main(sys.argv)
