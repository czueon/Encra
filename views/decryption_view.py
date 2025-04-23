from flask import Blueprint, render_template

decryption_view_bp = Blueprint('decryption_view', __name__)

@decryption_view_bp.route('/encrypt/decrypt', methods=['GET'])
def show_decrypt_page():
    return render_template('decrypt.html')
