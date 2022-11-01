# Copyright (C) 2022 Roberto Rossini <roberros@uio.no>
#
# SPDX-License-Identifier: MIT

import numpy as np

from cryptonite.decrypt import decrypt
from cryptonite.encrypt import encrypt


def test_encrypt():
    plain_text = "I am Superman. I stand for truth, for justice, and for the future."

    offset = 1
    expected = "J!bn!Tvqfsnbo/!J!tuboe!gps!usvui-!gps!kvtujdf-!boe!gps!uif!gvuvsf/"

    assert encrypt(plain_text, offset) == expected


def test_decrypt():
    encrypted_text = "Ajm\x1bompoc\x1b\\i_\x1bepnod^`\x1c"
    offset = -5

    expected = "For truth and justice!"

    assert decrypt(encrypted_text, offset) == expected


def test_encrypt_np():
    plain_text = "I am Superman. I stand for truth, for justice, and for the future."
    plain_text_np = np.fromiter(plain_text.encode("ascii"), dtype=np.uint8)

    offset = 1
    expected = "J!bn!Tvqfsnbo/!J!tuboe!gps!usvui-!gps!kvtujdf-!boe!gps!uif!gvuvsf/"

    assert encrypt(plain_text_np, offset) == expected


def test_decrypt_np():
    encrypted_text = "Ajm\x1bompoc\x1b\\i_\x1bepnod^`\x1c"
    encrypted_text_np = np.fromiter(encrypted_text.encode("ascii"), dtype=np.uint8)
    offset = -5

    expected = "For truth and justice!"

    assert decrypt(encrypted_text_np, offset) == expected
