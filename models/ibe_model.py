from models.pkg_model import kem_encrypt, kem_decrypt
from models.aes_model import aes_encrypt, aes_decrypt

# KEM + DEM 방식 기반 IBE 구조

# 이미지 암호화
def encrypt_aes_key(email: str, image_bytes: bytes) -> tuple[bytes, bytes]:
    # 1. KEM: 공유 대칭키, U (g^r)
    shared_key, U_bytes = kem_encrypt(email)

    # 2. DEM: AES-GCM으로 이미지 암호화
    encrypted_image = aes_encrypt(image_bytes, shared_key)

    return encrypted_image, U_bytes

# 이미지 복호화
def decrypt_aes_key(email: str, encrypted_image: bytes, U_bytes: bytes) -> bytes:
    # 1. KEM: 공유 대칭키 복원
    shared_key = kem_decrypt(email, U_bytes)

    # 2. DEM: 이미지 복호화
    decrypted_image = aes_decrypt(encrypted_image, shared_key)

    return decrypted_image