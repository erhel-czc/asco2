from pwdlib import PasswordHash

password_hash = PasswordHash.recommended()


def hash_password(plain: str) -> str:
    """Return a secure hash of a plaintext password."""
    return password_hash.hash(plain)


def verify_password(plain: str, hashed: str) -> bool:
    """Return True if plain matches the stored password hash."""
    return password_hash.verify(plain, hashed)
