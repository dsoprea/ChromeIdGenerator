ChromeIdGenerator
=================

A tiny tool to generate Google Chrome extension IDs from an extension's 
public-key.

Details
=======

Google Chrome calculates its extension-IDs by applying the "mpdecimal" scheme 
to the public PEM-formatted key of each extension.

The following is the algorithm:

1) If your PEM-formatted public-key still has the header and footer and is 
   split into multiple lines, reformat it by hand so that you have a single 
   string of characters that excludes the header and footer, and runs together
   such that every line of the key wraps to the next.
2) Base64-decode the public key to render a DER-formatted public-key.
3) Generate a SHA256 hex-digest of the DER-formatted key.
4) Take the first 32-bytes of the hash. You will not need the rest.
5) For each [hex] character, convert it to base-10 ('3' => 3, 'a' => 10), and 
   add the ASCII code for 'a'.

Example
=======

The PEM, public key for the "JSONView" extension has been stored to file 
"jsonview_public_pem.txt":

-----BEGIN PUBLIC KEY-----
MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQCsTeRKuxevWiein7geQszhb8mH
RpLByZbXX8tR0m1GPBkN8SN9xgo7NijAYAqa3H5rGuDmNZm2k7UzdlVfC5+gO6uf
/rVOPx7kHJNQBQaBuWUEd4KHLWa3jOy+mllD72TwXNdtJJdX6TWf115SGHlLzZRg
7S47dke6KTZI6O8gcQIDAQAB
-----END PUBLIC KEY-----

$ ./extension_id.py jsonview_public_pem.txt
Converting PEM-formatted public key to DER-formatted key.
Distilled PEM:

MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQCsTeRKuxevWiein7geQszhb8mHRpLByZbXX8tR0m1GPBkN8SN9xgo7NijAYAqa3H5rGuDmNZm2k7UzdlVfC5+gO6uf/rVOPx7kHJNQBQaBuWUEd4KHLWa3jOy+mllD72TwXNdtJJdX6TWf115SGHlLzZRg7S47dke6KTZI6O8gcQIDAQAB

Checking DER-formatted public key.
Building ID from DER-formatted public key.

Extension ID: chklaanhfefbnpoihckbnefhakgolnmc

Notes
=====

Please see SO article for additional details:

    http://stackoverflow.com/questions/16993486/how-to-programmatically-calculate-chrome-extension-id

