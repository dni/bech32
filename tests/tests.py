#!/usr/bin/python3
"""Reference tests for segwit adresses"""

import json
import unittest

from bech32 import bech32_encode

testdata = json.loads(open("./tests/fixtures.json").read())


class TestBech32Encode(unittest.TestCase):
    """Unit test class for Bech32 Encoding."""

    def test_encode(self):
        """Test Bech32 Encoding."""
        for valid in testdata.get("bech32").get("valid"):
            print(valid)
            bech32_encode(valid.get("prefix"), valid.get("string"))
            # self.assertEqual(bech32_encode("bc", b_string.encode()),
            #   "bc1qar0srrr7xfkvy5l643lydnw9re59gtzzwf5mdq")


if __name__ == "__main__":
    unittest.main()
