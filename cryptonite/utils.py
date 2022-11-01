# Copyright (C) 2022 Roberto Rossini <roberros@uio.no>
#
# SPDX-License-Identifier: MIT
import sys


def __is_ascii_py3(text) -> bool:
    if not isinstance(text, str):
        raise RuntimeError("text is not of str type.")

    try:
        text.encode("ascii")
    except UnicodeEncodeError:
        return False

    return True


def __is_ascii_py37(text) -> bool:
    if not isinstance(text, str):
        raise RuntimeError("text is not of str type.")

    return text.isascii()


def is_ascii(text) -> bool:
    """
    Return whether text is a valid ASCII string
    :param text:
    :return:
    """
    vmaj, vmin, _, _, _ = sys.version_info
    assert int(vmaj) == 3
    if int(vmin) >= 7:
        return __is_ascii_py37(text)

    return __is_ascii_py3(text)
