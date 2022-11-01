# Copyright (C) 2022 Roberto Rossini <roberros@uio.no>
#
# SPDX-License-Identifier: MIT

from typing import Union

import numpy as np

from cryptonite.encrypt import encrypt
from cryptonite.utils import is_ascii


def decrypt(text: Union[str, np.ndarray], offset: int, validate: bool = True) -> str:
    """
    Decrypt ASCII text by shifting each characted by the offset param.
    :param text: a string-like object containing encrypted text.
    :param offset: a non-zero integer. Multiples of 127 will raise an error.
    :param validate: validate input string.
    :return: plain text.
    """
    if isinstance(text, np.ndarray):
        validate = False

    if validate:
        if not is_ascii(text):
            raise RuntimeError("text does not use ASCII encoding.")

    num_ascii_chars = 127
    offset = offset % num_ascii_chars
    if offset == 0:
        return text

    return encrypt(text, -offset, validate)
