"""bech32 CLI"""


import click

from bech32 import bech32_decode, bech32_encode, Encoding

# disable tracebacks on exceptions
# sys.tracebacklimit = 0


@click.group()
def command_group():
    """
    Python CLI for bech32
    decode and encode bech32"""


@click.command()
@click.argument("hrp", type=str)
@click.argument("data", type=str)
@click.argument("spec", type=int)
def encode(hrp: str, data: str, spec: Encoding = Encoding.BECH32):
    """
    encode data
    """
    encoded = bech32_encode(hrp, data.encode(), spec)
    click.echo(encoded)


@click.command()
@click.argument("bech32_string", type=str)
def decode(bech32_string: str):
    """
    decode a bech32 string
    """
    hrp, data, spec = bech32_decode(bech32_string)
    click.echo(f"spec: {spec}")
    click.echo(f"hrp: {hrp}")
    click.echo(f"data: {data}")


def main():
    """main function"""
    command_group.add_command(encode)
    command_group.add_command(decode)
    command_group()


if __name__ == "__main__":
    main()
