from flask import Flask, render_template, request, flash, send_file, abort, redirect, url_for
from flask_login import LoginManager, login_required, current_user
from itsdangerous import URLSafeTimedSerializer, BadSignature, SignatureExpired
from models import db, File, User
from crypto_utils import encrypt_file, decrypt_file
from auth import auth_bp
import os

UPLOAD_FOLDER = "uploads"

app = Flask(__name__)
app.config["SECRET_KEY"] = "dev-secret-key-change-this"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

db.init_app(app)


app.register_blueprint(auth_bp)


login_manager = LoginManager()
login_manager.login_view = "auth.login"
login_manager.init_app(app)


serializer = URLSafeTimedSerializer(app.config["SECRET_KEY"])


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.route("/")
def home():
    return redirect(url_for("auth.login"))


@app.route("/dashboard", methods=["GET", "POST"])
@login_required
def dashboard():

    if request.method == "POST":
        uploaded_file = request.files.get("file")

        if uploaded_file and uploaded_file.filename != "":
            original_filename = uploaded_file.filename

            temp_path = os.path.join(app.config['UPLOAD_FOLDER'], original_filename)
            uploaded_file.save(temp_path)


            encrypted_filename, encrypted_key = encrypt_file(temp_path, current_user.public_key)

            file_record = File(
                filename=original_filename,
                stored_filename=encrypted_filename,
                encrypted_key=encrypted_key,
                user_id=current_user.id
            )

            db.session.add(file_record)
            db.session.commit()

            os.remove(temp_path)

            flash("File encrypted and stored securely")

    user_files = File.query.filter_by(user_id=current_user.id).all()
    files_with_tokens = []

    for file in user_files:
        token = serializer.dumps({"file_id": file.id, "user_id": current_user.id})
        files_with_tokens.append((file, token))

    return render_template("dashboard.html", files=files_with_tokens)


@app.route("/download/<int:file_id>")
@login_required
def download(file_id):

    token = request.args.get("token")
    if not token:
        abort(403)

    try:
        data = serializer.loads(token, max_age=60)
    except SignatureExpired:
        return "Download link expired", 403
    except BadSignature:
        return "Invalid download token", 403

    if data["file_id"] != file_id or data["user_id"] != current_user.id:
        return "Unauthorized access", 403

    file_record = File.query.get_or_404(file_id)
    decrypted_path = decrypt_file(file_record, current_user)

    return send_file(decrypted_path, as_attachment=True)


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
        os.makedirs(UPLOAD_FOLDER, exist_ok=True)

    app.run(debug=True)
