from discrete import rsa_crypt, rsa_decrypt, string_encode, string_decode
from rsa_private import private_key, public_keys


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
