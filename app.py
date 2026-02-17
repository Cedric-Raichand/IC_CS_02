from flask import Flask, redirect
from flask_login import LoginManager
from models import db, User
from auth import auth_bp
from dashboard_routes import dashboard_bp

app = Flask(__name__)
app.secret_key = "supersecretkey"

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)

login_manager = LoginManager()
login_manager.login_view = "auth.login"
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


app.register_blueprint(auth_bp)
app.register_blueprint(dashboard_bp)


@app.route("/")
def home():
    return redirect("/login")


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
