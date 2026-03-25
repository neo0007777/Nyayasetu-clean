import secrets
from cryptography.fernet import Fernet

if __name__ == "__main__":
    jwt_key = secrets.token_hex(32)
    enc_key = Fernet.generate_key().decode()

    print("=" * 55)
    print("NyayaSetu — Security Key Generator")
    print("=" * 55)
    print(f"\nJWT_SECRET_KEY={jwt_key}")
    print(f"\nENCRYPTION_KEY={enc_key}")
    print("\nPaste both into your .env file.")
    print("=" * 55)
