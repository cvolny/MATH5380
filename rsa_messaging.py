import random
from discrete import powermod
from rsa_private import *
from some_primes import SomePrimes

m = random.choice(SomePrimes)
sinc = ('Kyleigh', 'Srinivas', 'Nitun',)
# test run against my own
name = raw_input("Who are you? ")
print "Test run for you (%s) succeeded? %s" % (name, powermod(powermod(m, *rsa_keys[name]['public'][::-1]), b, n) in SomePrimes,)
print
print "Generating messages to %s:" % ", ".join(sinc)
print

msgs = {}
for key in [x for x in rsa_keys.keys() if x in sinc]:
    dest = "%s" % (key,)
    msgs[dest] = powermod(m, *rsa_keys[key]['public'][::-1])

print "to: field"
for key in msgs.keys():
    print "%s <%s>," % (key, rsa_keys[key]['email'],)
print

print "msg body:"
for k, v in msgs.iteritems():
    print "%s:\t%s" % (k, v)

