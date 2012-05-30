#!/usr/bin/env python
'''

Make a nice restructured text table from the output of get_tuple_info

Author: Evan K. Friis, UW Madison


'''
from RecoLuminosity.LumiDB import argparse
import json
from FinalStateAnalysis.Utilities.prettytable import PrettyTable

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('tuple_info',
                        help='JSON file with list of published PAT tuples')
    parser.add_argument('output', help='Output .txt file')

    args = parser.parse_args()

    x = PrettyTable(["AOD DBS", "PAT DBS", "Files", "Events"])

    x.set_field_align("AOD DBS", "l") # Left align city names
    x.set_field_align("PAT DBS", "l") # Left align city names
    x.set_padding_width(1) # One space between column edges and contents (default)==

    with open(args.tuple_info, 'r') as input:
        input_dict = json.load(input)
        for key in sorted(input_dict.keys()):
            val = input_dict[key]
            x.add_row([
                val['parent'],
                key,
                val['nfiles'],
                val['nevents'],
            ])

    with open(args.output, 'w') as output:
        output.write(str(x) + '\n')
