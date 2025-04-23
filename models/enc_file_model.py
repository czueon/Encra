import json
import base64

# .enc 파일 생성: base64 인코딩된 JSON 구조
def create_enc_file(encrypted_image: bytes, U_bytes: bytes) -> bytes:
    data = {
        "encrypted_image": base64.b64encode(encrypted_image).decode(),
        "U": base64.b64encode(U_bytes).decode()
    }
    return json.dumps(data).encode()

# .enc 파일 파싱: base64 디코딩하여 bytes로 복원
def parse_enc_file(enc_file_bytes: bytes) -> tuple[bytes, bytes]:
    try:
        if not enc_file_bytes:
            raise ValueError("빈 .enc 파일입니다.")

        data = json.loads(enc_file_bytes.decode())
        encrypted_image = base64.b64decode(data["encrypted_image"])
        U_bytes = base64.b64decode(data["U"])
        return encrypted_image, U_bytes

    except Exception as e:
        raise ValueError(f".enc 파일 파싱 실패: {str(e)}")
