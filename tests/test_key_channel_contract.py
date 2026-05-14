import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pytest

from aes_socket_utils import build_key_packet, parse_key_packet


def test_key_channel_contract_aes_128():
    key = b"a" * 16
    iv = b"b" * 16
    packet = build_key_packet(key, iv)

    assert packet[:4] == (16).to_bytes(4, "big")
    assert packet[4:20] == key
    assert packet[20:36] == iv

    parsed_key, parsed_iv = parse_key_packet(packet)
    assert parsed_key == key
    assert parsed_iv == iv


def test_key_channel_contract_aes_256():
    key = b"a" * 32
    iv = b"b" * 16
    packet = build_key_packet(key, iv)

    assert packet[:4] == (32).to_bytes(4, "big")
    parsed_key, parsed_iv = parse_key_packet(packet)
    assert parsed_key == key
    assert parsed_iv == iv


def test_invalid_key_size_should_fail():
    with pytest.raises(ValueError):
        build_key_packet(b"short", b"b" * 16)
