from premium_app import decrypt, encrypt, hash_password


def test_encrypt_roundtrip():
    data = b"secret notes"
    assert decrypt(encrypt(data)) == data


def test_hash_password_deterministic():
    salt, h1 = hash_password("pass")
    _, h2 = hash_password("pass", salt)
    assert h1 == h2
