import csv
import logging
import os
import sys
import timeit
from volny_magic import median

"""
This module will profile regcd and egcd and write the results to csv
"""

logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)

setupstmt = """
from volny_magic import random_length_pair, random_length
from discrete import egcd, regcd
"""

rcode = """
regcd(*random_length_pair({0}))
"""

icode = """
egcd(*random_length_pair({0}))
"""


def main():
    b, m = 100, 200
    inter = 10000
    cases = [x*100 for x in range(1,11)]
    width = len(str(max(cases)))
    with open(os.path.expanduser("~/Desktop/egcd_results.csv"), 'wbc') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(('N-Length','Recursive','Iterative'))
        csvfile.flush()
        for case in cases:
            rstmt = rcode.format(case)
            istmt = icode.format(case)
            r = median(timeit.Timer(rstmt, setup=setupstmt).repeat(inter, 1))
            i = median(timeit.Timer(istmt, setup=setupstmt).repeat(inter, 1))
            indx = ('{0:%sd}' % (width,)).format(case)
            rstr = '{0:0.15f}'.format(r)
            istr = '{0:0.15f}'.format(i)
            writer.writerow([indx, rstr, istr])
            csvfile.flush()


if "__main__" == __name__:
    main()
