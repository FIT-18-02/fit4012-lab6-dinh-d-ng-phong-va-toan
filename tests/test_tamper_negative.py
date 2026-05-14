import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pytest
from aes_socket_utils import encrypt_aes_cbc, decrypt_aes_cbc

def test_tampered_ciphertext_should_fail_or_change_plaintext():
    key = b"1" * 16
    iv = b"2" * 16
    plain = b"Secret message"
    _, _, ciphertext = encrypt_aes_cbc(plain, key=key, iv=iv)
    
    tampered = bytearray(ciphertext)
    tampered[-1] ^= 0x01
    
    with pytest.raises(Exception):
        decrypt_aes_cbc(key, iv, bytes(tampered))
