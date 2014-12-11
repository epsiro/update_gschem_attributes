#!/usr/bin/python

import csv
import re
import json

with open('test.csv', 'rb') as csv_file:

    component_reader = csv.reader(csv_file, delimiter=',', quotechar='"')

    for component in component_reader:
        print component
        #print ', '.join(row)

lines = (line.rstrip('\n') for line in open("filter.sch"))

components = {}
with open("filter.sch", "r") as sch_file:

    schem = sch_file.read()

    # Collect the number of characters we have read so far in the file
    # for a given line (list index). This gives the relationship between
    # number of chars read and which line we are on.
    char_on_line = []
    for m in re.finditer('.*\n', schem):
        char_on_line.append(m.end())

    prog = re.compile('\{([^}]+)\}')
    for match in prog.finditer(schem):

        refdes = ""
        component = {}

        # Get the line number for the start of the match
        match_start_line_nr = next(i for i in range(len(char_on_line)) if char_on_line[i] > match.start())

        attributes = match.group().split("\n")
        for i, attribute in enumerate(attributes):
            if attribute.startswith("refdes"):
                refdes = attribute
            if not attribute.startswith("T"):
                # Get the line number of the attribute
                component[attribute] = match_start_line_nr + i

        # If we found a component, add it to the list (dictionary)
        if refdes != "":
            components[refdes] = component

print json.dumps(components, sort_keys=True, indent=4)
