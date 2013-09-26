
import timeit

"""
This module will profile GCD and print out a CSV to be pasted into Excel.
"""

print("i,random,gcd")

for i in [100+i*20 for i in range(0,6)]:

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

    r = [str(x) for x in (i, t1, t2, t3,)]
    print(",".join(r))

