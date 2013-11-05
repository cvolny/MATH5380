#import random
from discrete import *
from rsa_private import *
#<editor-fold desc="Description">
#from some_primes import SomePrimes

#m = random.choice(SomePrimes)
#sinc = ('Kyleigh', 'Srinivas', 'Nitun',)
## test run against my own
#name = raw_input("Who are you? ")
#print "Test run for you (%s) succeeded? %s" % (name, powermod(powermod(m, *rsa_keys[name]['public'][::-1]), b, n) in SomePrimes,)
#print
#print "Generating messages to %s:" % ", ".join(sinc)
#print
#
#msgs = {}
#for key in [x for x in rsa_keys.keys() if x in sinc]:
#    dest = "%s" % (key,)
#    msgs[dest] = powermod(m, *rsa_keys[key]['public'][::-1])
#
#print "to: field"
#for key in msgs.keys():
#    print "%s <%s>," % (key, rsa_keys[key]['email'],)
#print
#
#print "msg body:"
#for k, v in msgs.iteritems():
#    print "%s:\t%s" % (k, v)
#</editor-fold>

#<editor-fold desc="Description">
#
## 0
#txmsg = """Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nullam in diam turpis. Quisque sed felis felis. Phasellus ut justo quis augue suscipit volutpat sed ac urna. Vivamus eget lobortis est. Fusce massa dui, tristique nec tempor in, mollis ut nibh. In ultricies lectus quis nunc feugiat egestas ut at purus. Cum sociis natoque penatibus et magnis dis parturient montes, nascetur ridiculus mus. Phasellus iaculis elementum elit eu venenatis. Nam at congue purus, quis tempor tellus. Integer tristique massa eu felis pretium condimentum. Fusce ut sagittis turpis, sed semper nunc. Donec interdum, sapien at lacinia facilisis, lacus risus euismod velit, vel pellentesque nunc sapien ac elit. Morbi consectetur pellentesque neque, vel vulputate nunc imperdiet in. Sed ornare felis cursus, dictum sapien ac, pretium massa. Curabitur condimentum purus quis lectus elementum cursus. Nam pretium magna ut pharetra iaculis.
#
#Vestibulum lacinia purus sed velit porta semper. Duis eleifend eu ligula in eleifend. Nullam convallis imperdiet ultrices. Aliquam fringilla, nisi sed porta fringilla, sapien augue ornare lectus, vel porttitor mi dolor auctor turpis. Suspendisse potenti. Pellentesque cursus tincidunt tortor feugiat sagittis. Praesent eget lobortis nisl. Sed eget mattis quam. Morbi hendrerit facilisis sodales. Fusce accumsan ante mi, in venenatis lorem consectetur in. Proin et nunc at tellus elementum tristique. Cras laoreet quis lectus ac mollis. Sed elementum sem eu quam ultricies, a ultricies felis condimentum. Praesent venenatis iaculis volutpat. Nullam pretium posuere nulla, ut pellentesque lacus elementum viverra."""

## 1
#txmsgc = string_encode(txmsg)
## 2
#txmsgcblks = digits(txmsgc, 100)
## 3
#txctextblks = []
#for txmsgcblk in txmsgcblks:
#    txctextblks.append(powermod(txmsgcblk, *public_keys['Chris']))
## 4
#ctext = horner(txctextblks, n)

#ctext = rsa_crypt(txmsg, *public_keys['Chris'], encoding=string_encode, encoding_block_size=100)
#rxmsg = rsa_decrypt(ctext, *private_key, decoding=string_decode, encoding_block_size=100)

## 4
#rxctextblks = digits(ctext, n)
#
## 3
#rxmsgcblks = []
#for rxctextblk in rxctextblks:
#    rxmsgcblks.append(powermod(rxctextblk, *private_key))
## 2
#rxmsgc = horner(rxmsgcblks, 100)
## 1
#rxmsg2 = string_decode(rxmsgc)
#assert rxmsg == rxmsg2

#print "0. txmsg:       %s" % txmsg
#print "1. txmsgc:      %s" % txmsgc
#print "2. txmsgcblks:  %d, %d" % (len(txmsgcblks), 100)
#print "3. txctextblks: %d" % len(txctextblks)
#print "4. ctext:       %s" % ctext
#print "3. rxctextblks: %d" % len(rxctextblks)
#print "2. rxmsgcblks   %d, %d" % (len(rxmsgcblks), 100)
#print "1. rxmsgc:      %s" % rxmsgc
#print "0. rxmsg:       %s" % rxmsg

#ctext = long(raw_input("Enter message text: "))
#blks = digits(ctext, n, rev=True)
#msgv = []
#for blk in blks:
#    msgv.append(powermod(blk, b, n))
#print msg
#</editor-fold>


def main():
    input_file = 'Samples/email.enc.txt'
    output_file = 'Samples/email.clear.txt'
    duplicate_file = 'Samples/email.enc2.txt'

    print "Reading file %s." % input_file
    with open(input_file, 'r') as f:
        contents = f.read()

    print "Decrypting message..."
    ctext = long(contents)
    msg = rsa_decrypt(ctext, *private_key, decode=string_decode)
    print "Results:"
    print msg
    print

    print "Writing cleartext results to %s." % output_file
    with open(output_file, 'w') as f:
        f.write(msg)

    print "Re-encrypting..."
    ctext2 = str(rsa_crypt(msg, *public_keys['Chris'], encode=string_encode))

    print "Writing encrypted results to %s." % duplicate_file
    with open(duplicate_file, 'wc') as f:
        f.write(ctext2)

    import filecmp
    print "Files are identical?", filecmp.cmp(input_file, duplicate_file)

if "__main__" == __name__:
    main()
