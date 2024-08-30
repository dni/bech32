""" wrapper for og bech32_encode with exceptions """

from .segwit_addr import Encoding
from .segwit_addr import bech32_encode as encode


def bech32_encode(hrp: str, data: list[int], spec: Encoding = Encoding.BECH32) -> str:
    encoded = encode(hrp, data, spec)
    return encoded
