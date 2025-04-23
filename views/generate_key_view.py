from flask import Blueprint, render_template

generate_key_view_bp = Blueprint('generate_key_view', __name__)

@generate_key_view_bp.route('/generate_key', methods=['GET'])
def show_generate_key_page():
    return render_template('generate_key.html')
