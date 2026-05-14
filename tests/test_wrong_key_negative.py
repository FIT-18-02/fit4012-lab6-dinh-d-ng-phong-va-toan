import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pytest
from aes_socket_utils import encrypt_aes_cbc, decrypt_aes_cbc

def test_wrong_key_should_not_recover_original_plaintext():
    key1 = b"1" * 16
    key2 = b"2" * 16
    iv = b"3" * 16
    plain = b"Secret message"
    _, _, ciphertext = encrypt_aes_cbc(plain, key=key1, iv=iv)
    
    with pytest.raises(Exception):
        decrypt_aes_cbc(key2, iv, ciphertext)
