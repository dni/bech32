"""Reference implementation for Bech32 and segwit addresses."""

from typing import Iterable, List, Tuple

from .exceptions import Bech32Exception

CHARSET = "qpzry9x8gf2tvdw0s3jn54khce6mua7l"
BECH32M_CONST = 0x2BC830A3


def bech32_polymod(values: Iterable[int]) -> int:
    """Internal function that computes the Bech32 checksum."""
    generator = [0x3B6A57B2, 0x26508E6D, 0x1EA119FA, 0x3D4233DD, 0x2A1462B3]
    chk = 1
    for value in values:
        top = chk >> 25
        chk = (chk & 0x1FFFFFF) << 5 ^ value
        for i in range(5):
            chk ^= generator[i] if ((top >> i) & 1) else 0
    return chk


def bech32_hrp_expand(hrp: str) -> List[int]:
    """Expand the HRP into values for checksum computation."""
    return [ord(x) >> 5 for x in hrp] + [0] + [ord(x) & 31 for x in hrp]


def bech32_verify_checksum(hrp: str, data: Iterable[int]) -> bool:
    """Verify a checksum given HRP and converted data characters."""
    return 1 == bech32_polymod(bech32_hrp_expand(hrp) + list(data))


def bech32m_verify_checksum(hrp: str, data: Iterable[int]) -> bool:
    """Verify a checksum given HRP and converted data characters."""
    return 2 == bech32_polymod(bech32_hrp_expand(hrp) + list(data))


def convertbits(
    data: Iterable[int], frombits: int, tobits: int, pad: bool = True
) -> List[int]:
    """General power-of-2 base conversion."""
    acc = 0
    bits = 0
    ret = []
    maxv = (1 << tobits) - 1
    max_acc = (1 << (frombits + tobits - 1)) - 1
    for value in data:
        if value < 0 or (value >> frombits):
            raise Bech32Exception("convertbits exception")
        acc = ((acc << frombits) | value) & max_acc
        bits += frombits
        while bits >= tobits:
            bits -= tobits
            ret.append((acc >> bits) & maxv)
    if pad:
        if bits:
            ret.append((acc << (tobits - bits)) & maxv)
    elif bits >= frombits or ((acc << (tobits - bits)) & maxv):
        raise Bech32Exception("convertbits exception")
    return ret


def create_checksum(hrp: str, const: int, data: Iterable[int]) -> List[int]:
    """Compute the checksum values given HRP and data."""
    values = bech32_hrp_expand(hrp) + list(data)
    polymod = bech32_polymod(values + [0, 0, 0, 0, 0, 0]) ^ const
    return [(polymod >> 5 * (5 - i)) & 31 for i in range(6)]


def build_encode(hrp: str, data: Iterable[int], checksum: List[int]) -> str:
    """Compute a Bech32 string given HRP and data values."""
    combined = list(data) + checksum
    return hrp + "1" + "".join([CHARSET[d] for d in combined])


def bech32m_encode(hrp: str, data: Iterable[int]) -> str:
    """Compute a Bech32m string given HRP and data values."""
    checksum = create_checksum(hrp, BECH32M_CONST, data)
    return build_encode(hrp, data, checksum)


def bech32_encode(hrp: str, string: str) -> str:
    """Compute a Bech32 string given HRP and data values."""
    data = string.encode("utf-8")
    checksum = create_checksum(hrp, 1, data)
    return build_encode(hrp, data, checksum)


def build_decode(bech: str) -> Tuple[str, List[int]]:
    """Validate a Bech32 string, and determine HRP and data."""
    if (any(ord(x) < 33 or ord(x) > 126 for x in bech)) or (
        bech.lower() != bech and bech.upper() != bech
    ):
        raise Bech32Exception("Bech32 Decode Exception")
    bech = bech.lower()
    pos = bech.rfind("1")
    if pos < 1 or pos > 83 or pos + 7 > len(bech):  # or len(bech) > 90:
        raise Bech32Exception("Bech32 Decode Exception")
    if not all(x in CHARSET for x in bech[pos + 1 :]):
        raise Bech32Exception("Bech32 Decode Exception")
    hrp = bech[:pos]
    data = [CHARSET.find(x) for x in bech[pos + 1 :]]
    return (hrp, data)


def bech32_decode(bech: str) -> Tuple[str, List[int], int]:
    """Validate a Bech32 string, and determine HRP and data."""
    hrp, data = build_decode(bech)
    if not bech32_verify_checksum(hrp, data):
        raise Bech32Exception("Bech32 Decode Verify Checksum Exception")
    return hrp, data[:-6], 1


def bech32m_decode(bech: str) -> Tuple[str, List[int], int]:
    """Validate a Bech32m string, and determine HRP and data."""
    hrp, data = build_decode(bech)
    if not bech32_verify_checksum(hrp, data):
        raise Bech32Exception("Bech32m Decode Verify Checksum Exception")
    return hrp, data[:-6], 2
