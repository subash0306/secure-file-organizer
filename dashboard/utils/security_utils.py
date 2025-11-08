import os
from cryptography.fernet import Fernet
from django.conf import settings


KEY_PATH = os.path.join(settings.BASE_DIR, "secret.key")

def generate_key():
    key = Fernet.generate_key()
    with open(KEY_PATH, "wb") as f:
        f.write(key)


def load_key():
    if not os.path.exists(KEY_PATH):
        generate_key()
    with open(KEY_PATH, "rb") as f:
        return f.read()


def encrypt_file(src_path):
    
    if not os.path.exists(src_path):
        raise FileNotFoundError(f"Source file not found: {src_path}")

    key = load_key()
    fernet = Fernet(key)

    with open(src_path, "rb") as f:
        data = f.read()

    encrypted_data = fernet.encrypt(data)

    filename = os.path.basename(src_path)
    enc_path = os.path.join(settings.MEDIA_ROOT, "encrypted", filename)

    os.makedirs(os.path.dirname(enc_path), exist_ok=True)

    with open(enc_path, "wb") as f:
        f.write(encrypted_data)

    print(f"[ENCRYPTED] {src_path} -> {enc_path}")
    return enc_path


def decrypt_file(src_path):
    
    key = load_key()
    fernet = Fernet(key)

    if not os.path.exists(src_path):
        raise FileNotFoundError(f"Encrypted file not found: {src_path}")

    with open(src_path, "rb") as f:
        encrypted_data = f.read()

    try:
        decrypted_data = fernet.decrypt(encrypted_data)
    except Exception as e:
        raise Exception(f"Decryption failed: {e}")

    rel_path = os.path.relpath(src_path, os.path.join(settings.MEDIA_ROOT, "encrypted"))
    parts = rel_path.split(os.sep)

    if len(parts) > 1:
        category = parts[0]  
        filename = parts[-1]
        output_dir = os.path.join(settings.MEDIA_ROOT, "decrypted", category)
    else:
        filename = parts[0]
        output_dir = os.path.join(settings.MEDIA_ROOT, "decrypted")

    os.makedirs(output_dir, exist_ok=True)

    dec_path = os.path.join(output_dir, filename)

    with open(dec_path, "wb") as f:
        f.write(decrypted_data)

    print(f"[DECRYPTED] {src_path} -> {dec_path}")
    return dec_path