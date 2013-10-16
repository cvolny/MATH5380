import logging
import os
import random
import sys
import timeit
from volny_magic import median, random_length #, tosn
from discrete import count_gcd

"""
This module will profile GCD and write out to CSVs for further analysis in LibreOffice Calc.

I don't use magic here, I use the actual timeit module (so capturing and processing results are quicker.

TODO:
    - further debug randint() errors for 2nd tests (see random_length() comment)
    - add matplotlib support to eliminate 3rd party spreadsheet
    - convert to numpy functions
    - cleanup logging facility
"""

logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)


def main():
    cases = [j*100 for j in range(1,11)]
    results = []

    # repeat 10k times and grab minimum runtimes. Track random gen separate from gcd time.
    for i in cases:
        statement = '10**{}'.format(i)
        t1 = min(timeit.Timer(statement).repeat(10000,1))
        setup = '''
import random
low = 10**{0}
high = 10**{1}-1
    '''.format(i, i+1)
        statement = 'random.randint(low, high)'
        t2 = min(timeit.Timer(statement, setup=setup).repeat(10000, 1))
        setup += '''
from main import gcd
a = {0}
b = {0}
    '''.format(statement,)
        statement = 'gcd(a, b)'
        t3 = min(timeit.Timer(statement, setup=setup).repeat(10000, 1))
        r = [str(x) for x in (i, t2, t3,)]
        results.append(",".join(r))


    with open(os.path.expanduser("~/Desktop/gcd_results.csv"), "w") as f:
        f.write("i,random,gcd\n")
        f.write("\n".join(results))

    results = []

    # Run 100 subcases per case value and grab the median count.
    for i in cases:
        subcases = range(100)
        subcases_count = len(subcases)
        counts = [1]*subcases_count
        for j in subcases:
            # use random_length(i) here to avoid low entropy errors on Intel Core2
                # needs further investigation to why above method won't work here
            a = random_length(i)
            b = random_length(i)
            c = count_gcd(a,b)
            #logging.debug('count_gcd(%s,%s) = %d' % (tosn(a), tosn(b), c,))
            subcases[j] = c
        results.append('%d,%s' % (i, str(median(subcases)),))

    with open(os.path.expanduser("~/Desktop/gcd_count_results.csv"), "w") as f:
        f.write("i,count\n")
        f.write("\n".join(results))

if "__main__" == __name__:
    main()
