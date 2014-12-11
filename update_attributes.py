#!/usr/bin/python

import csv

with open('test.csv', 'rb') as csv_file:

    component_reader = csv.reader(csv_file, delimiter=',', quotechar='"')

    for component in component_reader:
        print component
        #print ', '.join(row)
