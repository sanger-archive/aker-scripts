#!/usr/bin/env python

"""Generate a string that can be used for a JWT key."""

from jwcrypto.jwk import JWK

print(JWK.generate(kty='oct', size=2048).get_op_key())
