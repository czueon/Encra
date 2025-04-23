from flask import Flask, render_template
from controllers.encrypt_controller import encryption_bp
from controllers.decrypt_controller import decryption_bp
from controllers.generate_key_controller import generate_key_bp
from views.encryption_view import encryption_view_bp
from views.decryption_view import decryption_view_bp
from views.generate_key_view import generate_key_view_bp
from dotenv import load_dotenv # type: ignore
import os

load_dotenv()

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = os.getenv("SECRET_KEY")
    app.config['UPLOAD_FOLDER'] = os.getenv("UPLOAD_FOLDER")
    app.config['MAX_CONTENT_LENGTH'] = int(os.getenv("MAX_FILE_SIZE"))
    
    # Blueprint 등록
    app.register_blueprint(encryption_bp)
    app.register_blueprint(decryption_bp)
    app.register_blueprint(generate_key_bp)
    app.register_blueprint(encryption_view_bp)
    app.register_blueprint(decryption_view_bp)
    app.register_blueprint(generate_key_view_bp)


    @app.route('/')
    def index():
        return render_template("index.html")

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
