from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes

# AES 키 생성
def generate_aes_key():
    return get_random_bytes(32)  # AES-256

# AES 암호화(무결성 검증 태그 포함)
def aes_encrypt(data: bytes, key: bytes) -> bytes:
    cipher = AES.new(key, AES.MODE_GCM)  # GCM 인증(무결성 검증)
    ciphertext, tag = cipher.encrypt_and_digest(data)
    return cipher.nonce + tag + ciphertext  # 암호화 데이터 구조: [nonce][tag][ciphertext]

# AES 복호화 및 무결성 검사
def aes_decrypt(encrypted_data: bytes, key: bytes) -> bytes:
    nonce = encrypted_data[:16]       # 초기화 벡터
    tag = encrypted_data[16:32]       # GCM 인증 태그
    ciphertext = encrypted_data[32:]  # 암호문
    cipher = AES.new(key, AES.MODE_GCM, nonce=nonce)
    return cipher.decrypt_and_verify(ciphertext, tag)
