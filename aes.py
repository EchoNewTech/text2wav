import os
import base64
import pyaes
'''
Moduł do szyfrowania i deszyfrowania AES-CBC z użyciem hasła.
Wykorzystuje bibliotekę pyaes (czysta implementacja w Pythonie).'''

def _derive_key(password: str, key_len: int = 16) -> bytes:
    '''
    Prosta funkcja do wyprowadzenia klucza AES z hasła.
    Używa UTF-8 i dopasowuje długość klucza przez obcięcie lub dopełnienie zerami.
    '''
    b = password.encode("utf-8")
    if len(b) >= key_len:
        return b[:key_len]
    return b.ljust(key_len, b'\0')


def _pad(data: bytes, block_size: int = 16) -> bytes:
    '''
    Dodaje PKCS#7 padding do danych.'''
    pad_len = block_size - (len(data) % block_size)
    return data + bytes([pad_len]) * pad_len


def _unpad(data: bytes) -> bytes:
    '''
    Usuwa PKCS#7 padding z danych.
    '''
    if not data:
        raise ValueError("Brak danych do odpakowania")
    pad_len = data[-1]
    if pad_len < 1 or pad_len > 16:
        raise ValueError("Nieprawidłowy padding")
    if data[-pad_len:] != bytes([pad_len]) * pad_len:
        raise ValueError("Nieprawidłowy padding")
    return data[:-pad_len]


def encrypt_aes(plaintext: str, password: str) -> str:
    '''
    Szyfruje tekst za pomocą AES-CBC i zwraca wynik w formacie base64.
    '''
    key = _derive_key(password, 16)   # AES-128
    iv = os.urandom(16)
    aes = pyaes.AESModeOfOperationCBC(key, iv=iv)
    padded = _pad(plaintext.encode("utf-8"))
    ciphertext = aes.encrypt(padded)
    return base64.b64encode(iv + ciphertext).decode("utf-8")


def decrypt_aes(encrypted_b64: str, password: str) -> str:
    '''
    Odszyfrowuje tekst zaszyfrowany AES-CBC z formatu base64.
    Zwraca odszyfrowany tekst.
    '''
    try:
        raw = base64.b64decode(encrypted_b64.encode("utf-8"))
        if len(raw) < 16:
            raise ValueError("Za krótkie dane")
        iv, ciphertext = raw[:16], raw[16:]
        key = _derive_key(password, 16)
        aes = pyaes.AESModeOfOperationCBC(key, iv=iv)
        decrypted_padded = aes.decrypt(ciphertext)
        decrypted = _unpad(decrypted_padded)
        return decrypted.decode("utf-8")
    except Exception:
        raise ValueError("Nieprawidłowe hasło lub dane.")
