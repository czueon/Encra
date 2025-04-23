from flask import Blueprint, request, send_file
from models.ibe_model import encrypt_aes_key
from models.enc_file_model import create_enc_file
import tempfile

encryption_bp = Blueprint('encryption', __name__)

@encryption_bp.route('/encrypt', methods=['POST'])
def encrypt_image():
    image = request.files['image']
    email = request.form['email'].strip().lower()

    # 이미지 바이트 읽기
    image_bytes = image.read()
    if not image_bytes:
        raise ValueError("업로드된 이미지가 비어 있습니다.")

    # 암호화 (KEM + DEM): 암호화된 이미지, U(g^r)
    encrypted_image, U_bytes = encrypt_aes_key(email, image_bytes)

    # .enc 파일로 패킹
    enc_data = create_enc_file(encrypted_image, U_bytes)

    # 임시 파일로 저장
    tmp_path = tempfile.mktemp(suffix=".enc")
    with open(tmp_path, 'wb') as f:
        f.write(enc_data)

    return send_file(tmp_path, as_attachment=True, download_name="encrypted.enc")
