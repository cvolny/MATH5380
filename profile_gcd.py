import csv
import logging
import os
import sys
import timeit
from volny_magic import median


"""
This module will profile gcd and write the results to csv
"""

logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)

setupstmt = """
from volny_magic import random_length_pair, random_length
from discrete import egcd, regcd
"""

icode = """
egcd(*random_length_pair({0}))
"""


def main():
    inter = 10000
    cases = [x*100 for x in range(1,11)]
    width = len(str(max(cases)))
    with open(os.path.expanduser("~/Desktop/gcd_results.csv"), 'wbc') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(('N-Length', 'GCD'))
        for case in cases:
            istmt = icode.format(case,)
            i = median(timeit.Timer(istmt, setup=setupstmt).repeat(inter, 1))
            indx = ('{0:%sd}' % (width,)).format(case)
            istr = '{0:0.15f}'.format(i)
            writer.writerow([indx, istr])
            csvfile.flush()

if "__main__" == __name__:
    main()
