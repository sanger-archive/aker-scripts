#!/usr/bin/env python

# Generates a string can be used for a JWT key
import jwcrypto.jwk as jwk
key = eval(jwk.JWK.generate(kty='oct', size=2048).export())

print(key["k"])

