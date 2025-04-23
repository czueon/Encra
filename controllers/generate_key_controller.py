import os
from flask import Blueprint, request
from models.pkg_model import generate_master_keys, extract_user_private_key
from dotenv import load_dotenv

load_dotenv()

USER_KEY_DIR = os.getenv("USER_KEY_DIR")
generate_key_bp = Blueprint('generate_key', __name__)

@generate_key_bp.route('/generate_key', methods=['POST'])
def generate_key():
    email = request.form['email'].strip().lower()
    
    # 마스터 키 최초 1회 생성
    generate_master_keys()

    # 개인키 생성 (bytes 형태)
    sk_id = extract_user_private_key(email)

    # 저장 경로 생성
    os.makedirs(USER_KEY_DIR, exist_ok=True)
    key_path = os.path.join(USER_KEY_DIR, f"{email}.key")

    # 개인키 저장 (bytes → hex string)
    with open(key_path, 'w') as f:
        f.write(sk_id.hex())

    return f"개인키가 서버에 안전하게 저장되었습니다."
