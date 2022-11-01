#!/usr/bin/env python

# Copyright (C) 2022 Roberto Rossini <roberros@uio.no>
#
# SPDX-License-Identifier: MIT

from __future__ import absolute_import

import argparse
import os
import sys
from typing import Union

try:
    from importlib.metadata import version
except ModuleNotFoundError:
    from importlib_metadata import version

import numpy as np

from . import decrypt, encrypt


def read_key_from_env() -> Union[str, None]:
    return os.environ.get("CRYPTONITE_KEY")


def make_cli() -> argparse.ArgumentParser:
    cli = argparse.ArgumentParser()
    subparsers = cli.add_subparsers(help="subcmd", dest="command")
    encrypt_cmd = subparsers.add_parser("encrypt", help="Encrypt message received from stdin and output to stdout.")

    decrypt_cmd = subparsers.add_parser("decrypt", help="Decrypt message received from stdin and output to stdout.")

    ver = version("2022-sbi-ci-workflow-cryptonite-mingyi")
    for cmd in [cli, decrypt_cmd, encrypt_cmd]:
        cmd.add_argument("--version", action="version", version=f"%(prog)s v{ver}")

    for cmd in [decrypt_cmd, encrypt_cmd]:
        cmd.add_argument("--validate-input", action="store_true")
        cmd.add_argument("--no-validate-input", dest="validate_input", action="store_false")
        cmd.set_defaults(validate_input=True)

    key_required = read_key_from_env() is None
    encrypt_cmd.add_argument("-k", "--key", type=int, help="Encryption key.", required=key_required)
    decrypt_cmd.add_argument("-k", "--key", type=int, help="Decryption key.", required=key_required)

    return cli


def parse_and_validate_args(cli) -> Union[dict, None]:
    args = vars(cli.parse_args())
    if args["command"] is None:
        cli.print_help()
        return None

    if args["key"] is None:
        key = read_key_from_env()
        if key is None:
            raise RuntimeError("Failed to read key from CRYPTONITE_KEY env variable")
        args["key"] = int(key)

    return args


def __read_next_chunk(chunk_size: int = 64 * 1024 * 1024 / 8) -> str:
    assert int(chunk_size) > 0
    return sys.stdin.read(int(chunk_size))


def __read_next_chunk_np(chunk_size: int = 64 * 1024 * 1024 / 8) -> np.ndarray:
    chunk = __read_next_chunk(chunk_size).encode("ascii")
    return np.fromiter(chunk, count=len(chunk), dtype=np.uint8)


def main() -> int:
    cli = make_cli()

    try:
        args = parse_and_validate_args(cli)
        if not args:
            return 1
    except RuntimeError as excp:
        print(f"CLI parsing failed with the following error: {excp}", file=sys.stderr)
        return 1

    validate_input = args["validate_input"]
    if validate_input:
        sys.stdin.reconfigure(encoding="utf-8")
        read_next_chunk = __read_next_chunk
    else:
        sys.stdin.reconfigure(encoding="ascii")
        read_next_chunk = __read_next_chunk_np

    key = args["key"]
    assert key

    if args["command"] == "encrypt":
        operator = encrypt.encrypt
    else:
        assert args["command"] == "decrypt"
        operator = decrypt.decrypt

    try:
        buff = read_next_chunk()
        while len(buff) != 0:
            sys.stdout.write(operator(buff, key, validate_input))
            buff = read_next_chunk()

    except RuntimeError as excp:
        operation = args["command"].capitalize() + "ion"
        print(f"{operation} failed due to the following error: {excp}", file=sys.stderr)
        return 1

    return 0


if __name__ == "__main__":
    main()
