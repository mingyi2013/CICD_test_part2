# Copyright (C) 2022 Roberto Rossini <roberros@uio.no>
#
# SPDX-License-Identifier: MIT
from typing import Union

import numpy as np

from cryptonite.utils import is_ascii


def __encrypt_char(char: str, offset: int, num_ascii_chars: int = 127):
    return chr(abs((ord(char) + offset) % num_ascii_chars))


def __encrypt_np_array(text: np.ndarray, offset: int, num_ascii_chars: int = 127):
    return (text + offset) % num_ascii_chars


def encrypt(text: Union[str, np.ndarray], offset: int, validate: bool = True) -> str:
    """
    Encrypt ASCII text by shifting each characted by the offset param.
    :param text: a string-like object with the message to be encrypted. Should not contain non-ASCII characters.
    :param offset: a non-zero integer. Multiples of 127 will raise an error.
    :param validate: validate input string.
    :return: encrypted text
    """
    if isinstance(text, np.ndarray):
        validate = False

    num_ascii_chars = 127

    if validate:
        if not is_ascii(text):
            raise RuntimeError("text does not use ASCII encoding.")

        if offset == 0:
            raise RuntimeError("invalid offset: offset must be a non-zero integral number")

        if offset % num_ascii_chars == 0:
            raise RuntimeError(
                f"invalid offset: offset is a multiple of {num_ascii_chars}."
                " Encrypted text would be identical to plain text!"
            )

    offset %= num_ascii_chars
    if isinstance(text, np.ndarray):
        return __encrypt_np_array(text, offset).tobytes().decode("ascii")

    return "".join(map(str, [__encrypt_char(c, offset) for c in text]))
