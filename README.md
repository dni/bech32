bech32
======

bech32/bech32m encoding/decoding library and cli tool. BIP173/BIP350 compatible.
based on sipa's bech32 forked by rustyrussell, fiatjaf and lnbits.


notes
----

Forked from `rustyrussell/lightning-payencode` and published on PyPI.
The original version of this package is probably the one at `sipa/bech32` but apparently Rusty Russel
commented out the 90-length limit of bech32-encoded stuff so it could be used for Lightning invoices.


resources
--------

* [sipa/bech32](https://github.com/sipa/bech32/tree/master/ref/python)
* [rustyrussell/lightning-encode](https://github.com/rustyrussell/lightning-payencode)
* [BIP173](https://github.com/bitcoin/bips/blob/master/bip-0173.mediawiki)
* [BIP350](https://github.com/bitcoin/bips/blob/master/bip-0350.mediawiki)
* [PyPI](https://pypi.org/project/bech32/)


Install
-------

```
poetry install
```
run cli
```
poetry run bech32 decode tb1aaaaaaaaaaaaaaaaaaaaaa
poetry run bech32 encode tb helloworld
```
