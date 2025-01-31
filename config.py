from datetime import date

ADULT_COUNT = 1
CHILD_COUNT = 0
ROOM_COUNT = 1
RESULT_COUNT = 30
CHECK_IN = date(2019, 6, 1)
CHECK_OUT = date(2019, 6, 2)
HEADERS = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'\
            ' AppleWebKit/537.36 (KHTML, like Gecko)'\
            ' Chrome/70.0.3538.77 Safari/537.36',
    'accept': '*/*',
    'accept-language': 'en-US, en;q=0.5',
    'connection': 'keep-alive',
    'x-requested-with': 'XMLHttpRequest',
}
CURRENCY = {
        'sf': 'USD',
        'ny': 'USD',
        'tor': 'CAD',
        'lon': 'GBP',
        'am': 'EUR',
        'frank': 'EUR',
        'ban': 'INR',
        'sin': 'SGD',
}
LOCATION = {
        'sf': 'San+Francisco',
        'ny': 'New+York',
        'tor': 'Toronto',
        'lon': 'London',
        'am': 'Amsterdam',
        'frank': 'Frankfurt',
        'ban': 'Bangalore',
        'sin': 'Singapore',
}
OUTPUT_FILE = 'data.csv'
