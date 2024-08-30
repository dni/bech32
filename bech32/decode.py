""" wrapper for og bech32_decode with exceptions """

from .exceptions import Bech32Exception
from .segwit_addr import Encoding
from .segwit_addr import bech32_decode as decode


# https://github.com/rustyrussell/lightning-payencode/blob/master/bech32.py#L69
# rusty commented out the max size of the bech32 string for lightning invoices
# we set it to an arbitrary limit
def bech32_decode(bech: str, limit: int = 2**16) -> tuple[str, list[int], Encoding]:
    hrp, data, encoding = decode(bech, limit)
    if not hrp or not data or not encoding:
        raise Bech32Exception("Invalid bech32 string")
    return hrp, data, encoding
