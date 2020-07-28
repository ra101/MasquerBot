"""
./app/utils.py

This code is modified version of code in from utils.py from ecies. 
"""
import codecs


def remove_0x(s: str) -> str:
    if s.startswith("0x") or s.startswith("0X"):
        return s[2:]
    return s


def decode_hex(s: str) -> bytes:
    return codecs.decode(remove_0x(s), "hex")  # type: ignore
