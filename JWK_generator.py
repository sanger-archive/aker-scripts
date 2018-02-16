#!/usr/bin/env python

# Generates a string can be used for a JWT key
import jwcrypto.jwk as jwk
from ast import literal_eval

key = literal_eval(jwk.JWK.generate(kty='oct', size=2048).export())

print(key["k"])

