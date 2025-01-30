from cryptography.fernet import Fernet
import os

ENCRYPTION_KEY = os.getenv('DATA_ENCRYPTION_KEY', b'32bytehardcodedkey__change')

def encrypt_data(plaintext: str) -> str:
    f = Fernet(ENCRYPTION_KEY)
    return f.encrypt(plaintext.encode()).decode()

def decrypt_data(ciphertext: str) -> str:
    f = Fernet(ENCRYPTION_KEY)
    return f.decrypt(ciphertext.encode()).decode()

def generate_password(length=16, use_special=True):
    import string, random
    chars = string.ascii_letters + string.digits
    if use_special:
        chars += "!@#$%^&*()-_=+"
    return ''.join(random.choice(chars) for _ in range(length))
