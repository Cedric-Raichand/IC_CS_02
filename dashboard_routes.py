from flask import Blueprint, render_template, request, flash, send_file
from flask_login import login_required, current_user
from models import db, File
from crypto_utils import encrypt_file, decrypt_file
import os

dashboard_bp = Blueprint("dashboard", __name__)

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


@dashboard_bp.route("/dashboard", methods=["GET", "POST"])
@login_required
def dashboard():

    if request.method == "POST":
        uploaded_file = request.files.get("file")

        if uploaded_file and uploaded_file.filename != "":
            original_filename = uploaded_file.filename
            temp_path = os.path.join(UPLOAD_FOLDER, original_filename)
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

    files = File.query.filter_by(user_id=current_user.id).all()
    return render_template("dashboard.html", files=files)


@dashboard_bp.route("/download/<int:file_id>")
@login_required
def download(file_id):
    file_record = File.query.get_or_404(file_id)

    if file_record.user_id != current_user.id:
        return "Unauthorized access", 403

    decrypted_path = decrypt_file(file_record, current_user)
    return send_file(decrypted_path, as_attachment=True)
