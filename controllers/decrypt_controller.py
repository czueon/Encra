from flask import Blueprint, request, send_file
from models.ibe_model import decrypt_aes_key
from models.enc_file_model import parse_enc_file
import tempfile

decryption_bp = Blueprint('decryption', __name__)

@decryption_bp.route('/encrypt/decrypt', methods=['POST'])
def decrypt_image():
    enc_file = request.files['encfile']
    email = request.form['email'].strip().lower()

    enc_bytes = enc_file.read()
    if not enc_bytes:
        raise ValueError(".enc 파일이 비어 있습니다.")

    # .enc 파일 파싱 → (암호화된 이미지, U)
    encrypted_image, U_bytes = parse_enc_file(enc_bytes)

    # 복호화 수행
    decrypted_image = decrypt_aes_key(email, encrypted_image, U_bytes)

    # 임시 파일로 저장
    tmp_path = tempfile.mktemp(suffix=".jpg")
    with open(tmp_path, 'wb') as f:
        f.write(decrypted_image)

    return send_file(tmp_path, as_attachment=True, download_name="decrypted.jpg")
