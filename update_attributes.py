#!/usr/bin/python

import csv
import re
import json

csv_components = {}
with open('test.csv', 'rb') as csv_file:

    component_reader = csv.DictReader(csv_file, delimiter=',', quotechar='"')

    for component in component_reader:
        for refdes in component['refdes'].split(","):
            component.pop("refdes", None)
            component.pop("qty", None)
            csv_components[refdes] = component

print json.dumps(csv_components, sort_keys=True, indent=4)


def get_component_from_sch(schematic_file, subcircuit=""):
    components = {}
    with open(schematic_file, "r") as sch_file:

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
                if not attribute.startswith(("T", "{", "}")):
                    # Get the line number of the attribute
                    component[attribute.split("=")[0]] = match_start_line_nr + i

            # If we found a component, add it to the list (dictionary)
            if refdes != "":
                if subcircuit != "":
                    subcircuit_refdes = subcircuit + "/" + refdes.split("=")[1]
                else:
                    subcircuit_refdes = refdes.split("=")[1]

                components[subcircuit_refdes] = component

    #print json.dumps(components, sort_keys=True, indent=4)
    return components

with open("schematics", "r") as schs_file:
    for schematic in schs_file.readlines():
        schematic = schematic.split(",")
        subcircuit = schematic[0]
        schematic_file = schematic[1].strip()

        if subcircuit != "":

            sch_components = get_component_from_sch(schematic_file, subcircuit)

            with open(schematic_file, "r") as sch_file:
                data = sch_file.readlines()

                for refdes, attributes in sch_components.iteritems():
                    if refdes in csv_components:
                        for attribute in attributes:
                            #print csv_components[refdes]
                            if attribute in csv_components[refdes]:
                                attribute_line_number = sch_components[refdes][attribute]
                                new_attribute = csv_components[refdes].pop(attribute, None)
                                data[attribute_line_number] = attribute + "=" + new_attribute + "\n"
                        print refdes, "attributes not updated", csv_components[refdes]
                    else:
                        print "refdes " + refdes + " not found in csv"

            with open(schematic_file, 'w') as file:
                    file.writelines( data )
