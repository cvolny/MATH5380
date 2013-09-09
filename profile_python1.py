
from volny_magic import tosn
from factorial import ifactorial, rfactorial, binomial, ibinomial, rbinomial

for i in [10, 100, 250, 500, 750, 1000, 2500, 5000, 7500, 10000]:
    print "ifactorial(%d) = %s" % (i,tosn(ifactorial(i)))
    %timeit ifactorial(i)
    %memit ifactorial(i)
    print ""
    print "rfactorial(%d) = %s" % (i,tosn(rfactorial(i)))
    %timeit rfactorial(i)
    %memit rfactorial(i)
    print ""
    print ""


for i in [10, 100, 250, 500, 750, 1000, 2500, 5000, 7500, 10000]:
    j = min(i / 4, 25)
    print "binomial(%d,%d) = %s" % (i,j, tosn(binomial(i,j)))
    %timeit binomial(i,j)
    %memit binomial(i,j)
    print ""
    print "rbinomial(%d,%d) = %s" % (i,j, tosn(rbinomial(i,j)))
    %timeit binomial(i,j)
    %memit binomial(i,j)
    print ""
    print "ibinomial(%d,%d) = %s" % (i,j, tosn(ibinomial(i,j)))
    %timeit binomial(i,j)
    %memit binomial(i,j)
    print ""
    print ""

