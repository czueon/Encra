from flask import Blueprint, render_template

encryption_view_bp = Blueprint('encryption_view', __name__)

@encryption_view_bp.route('/encrypt', methods=['GET'])
def show_encrypt_page():
    return render_template('encrypt.html')
