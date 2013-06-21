#!/usr/bin/python
"""This module produces a Google Chrome extension ID. This ID is in a very 
elusive format that Google refers to as "mpdecimal".
"""

import sys
import hashlib
import select

from base64 import b64decode
from subprocess import Popen, PIPE

_be_verbose = False

def _info(message=''):
    if _be_verbose:
        print(message)

def validate_public_der(pub_key_der):
    _info("Checking DER-formatted public key.")

    command = ['openssl', 'rsa', '-inform', 'der', '-pubin', '-text']

    try:
        p = Popen(command, stdin=PIPE, stdout=PIPE, stderr=PIPE)
        p.communicate(input=pub_key_der)
    except:
        _info("ERROR: There was a problem accessing OpenSSL. Skipping check.")
        return True

    return (p.returncode == 0)

def convert_pem_to_der(pub_key_pem):
    """Convert a human-readable PEM certificate to a binary DER certificate. 
    This will trim the header and footer, if they're present, but they don't 
    have to be.
    """

    _info("Converting PEM-formatted public key to DER-formatted key.")

    pub_key_pem = pub_key_pem.strip()

    try:
        i = pub_key_pem.index("\n")
    except:
        pass
    else:
        pub_key_pem = pub_key_pem[i + 1:]

    try:
        i = pub_key_pem.rindex("\n")
    except:
        pass
    else:
        pub_key_pem = pub_key_pem[:i]

    pub_key_pem = pub_key_pem.replace("\r", '').replace("\n", '')

    _info("Distilled PEM:\n\n%s\n" % (pub_key_pem))

    return b64decode(pub_key_pem)

def build_id_from_der(pub_key_der):
    _info("Building ID from DER-formatted public key.")

    sha = hashlib.sha256(pub_key_der).hexdigest()
    prefix = sha[:32]

    reencoded = ""
    ord_a = ord('a')
    for old_char in prefix:
        code = int(old_char, 16)
        new_char = chr(ord_a + code)

        reencoded += new_char

    return reencoded

def main():
    global _be_verbose
    _be_verbose = True

    if len(sys.argv) < 2:
        pub_key_pem = sys.stdin.read()
    else:
        first_arg = sys.argv[1]
        if first_arg == '-h':
            print("Please pass a PEM-formatted public RSA key via STDIN, or "
                  "its file-path as the first argument. It does not need the "
                  "standard header or footer.")

            sys.exit(0)
        else:
            with file(first_arg) as f:
                pub_key_pem = f.read()

    pub_key_der = convert_pem_to_der(pub_key_pem)
    if validate_public_der(pub_key_der) is False:
        _info("Key is not a valid, PEM-formatted public key.")
        sys.exit(1)

    id_ = build_id_from_der(pub_key_der)

    _info()
    _info("Extension ID: %s" % (id_))

if __name__ == '__main__':
    main()

