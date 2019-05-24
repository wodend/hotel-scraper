#!/usr/bin/env python3

import csv
import time
from multiprocessing import Process, Queue

import config
import agoda
import booking
import hotels

queue = Queue()

for code in config.LOCATION:
    agoda_process = Process(target=agoda.scrape, args=(queue, code))
    booking_process = Process(target=booking.scrape, args=(queue, code))
    hotels_process = Process(target=hotels.scrape, args=(queue, code))
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
