from flask import Flask, redirect, url_for, request, render_template, flash
from flask_login import LoginManager, login_required, current_user
from werkzeug.utils import secure_filename
import os
from models import db, User
from auth import auth_bp
from crypto_utils import encrypt_file
from rsa_utils import encrypt_key
import base64

app = Flask(__name__)
app.config['SECRET_KEY'] = 'supersecretkey'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'

db.init_app(app)

login_manager = LoginManager()
login_manager.login_view = "auth.login"
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

app.register_blueprint(auth_bp)

@app.route("/")
def home():
    return redirect("/register")

@app.route("/dashboard", methods=["GET","POST"])
@login_required
def dashboard():
    if request.method == "POST":
        if "file" not in request.files:
            flash("No file selected")
            return redirect(request.url)

        file = request.files["file"]
        if file.filename == "":
            flash("No filename")
            return redirect(request.url)

        filename = secure_filename(file.filename)
        file_path = os.path.join("uploads", filename)
        file.save(file_path)

        # AES encryption
        key, enc_path = encrypt_file(file_path)

        # RSA encrypt AES key
        encrypted_key = encrypt_key(key, current_user.public_key)

        flash(f"Encrypted AES key: {encrypted_key}")
        return redirect("/dashboard")

    return render_template("dashboard.html")


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
        os.makedirs("uploads", exist_ok=True)
    app.run(debug=True)
