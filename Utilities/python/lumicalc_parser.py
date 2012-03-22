'''

Parses the CSV output of lumi calc to get the total luminosity.

'''

import csv

def get_total_lumi(csv_filename):
    file = open(csv_filename, 'r')
    reader = csv.DictReader(file)
    output = 0.
    for row in reader:
        output += float(row['Recorded(/ub)'])
    return output/1e6

if __name__ == "__main__":
    import sys
    print get_total_lumi(sys.argv[1])
