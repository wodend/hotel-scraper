#!/usr/bin/env python3

import csv
import requests
import time
from multiprocessing import Process, Queue

import config
import agoda
import booking
import hotels

queue = Queue()
url = 'http://data.fixer.io/api/latest'
query = {
    'access_key': '00b557900a5055f07b5703afce9df099',
    'symbols': 'EUR,USD,CAD,GBP,INR,SGD',
}
#response = requests.get(url, params=query)
#rate = response.json()['rates']
# rates on 2019-05-28
rate = {
    'EUR': 1,
    'USD': 1.116931,
    'CAD': 1.506685,
    'GBP': 0.882129,
    'INR': 78.05954,
    'SGD': 1.540751,
}

for code in config.LOCATION:
    agoda_process = Process(target=agoda.scrape, args=(queue, code, rate))
    booking_process = Process(target=booking.scrape, args=(queue, code, rate))
    hotels_process = Process(target=hotels.scrape, args=(queue, code, rate))
    agoda_process.start()
    booking_process.start()
    hotels_process.start()
    agoda_process.join()
    booking_process.join()
    hotels_process.join()
    with open(config.OUTPUT_FILE, 'a') as fp:
        writer = csv.writer(fp)
        while not queue.empty():
            row = queue.get()
            writer.writerow(row)
        time.sleep(10)
