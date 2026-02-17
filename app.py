import os
from flasgger import Swagger 
from flask import Flask, request, jsonify, render_template, redirect, url_for, session, abort
from flask_sqlalchemy import SQLAlchemy
import bcrypt
from functools import wraps
from datetime import datetime

app = Flask(__name__)
app.secret_key = "dev-secret-change-me"

# =========================
# CONFIG DB
# =========================
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)


# =========================
# MODELE UTILISATEUR
# =========================
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(180), unique=True, nullable=False)
    password_hash = db.Column(db.LargeBinary, nullable=False)
    role = db.Column(db.String(20), nullable=False, default="user")  # admin | user
    is_approved = db.Column(db.Boolean, nullable=False, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def check_password(self, plain: str) -> bool:
        return bcrypt.checkpw(plain.encode("utf-8"), self.password_hash)


# =========================
# INIT DB + ADMIN
# =========================
def init_db():
    db.create_all()

    admin = User.query.filter_by(role="admin").first()
    if not admin:
        email = "admin@demo.com"
        password = "demo123"
        pw_hash = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())
        admin = User(
            email=email,
            password_hash=pw_hash,
            role="admin",
            is_approved=True
        )
        db.session.add(admin)
        db.session.commit()
        print("✅ Admin créé:", email, "/", password)


with app.app_context():
    init_db()


# =========================
# HELPERS AUTH
# =========================
def current_user():
    uid = session.get("user_id")
    if not uid:
        return None
    return db.session.get(User, uid)


def login_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        u = current_user()
        if not u:
            return redirect(url_for("login"))
        if not u.is_approved:
            return render_template(
                "login.html",
                error="Compte en attente de validation par un administrateur."
            ), 403
        return fn(*args, **kwargs)
    return wrapper


def admin_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        u = current_user()
        if not u:
            return redirect(url_for("login"))
        if u.role != "admin":
            abort(403)
        return fn(*args, **kwargs)
    return wrapper


# =========================
# PAGES WEB
# =========================
@app.get("/")
def home():
    return render_template("index.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register.html")

    email = request.form.get("email", "").strip().lower()
    password = request.form.get("password", "")
    password2 = request.form.get("password2", "")

    if not email or not password:
        return render_template("register.html", error="Email et mot de passe requis."), 422
    if password != password2:
        return render_template("register.html", error="Les mots de passe ne correspondent pas."), 422
    if User.query.filter_by(email=email).first():
        return render_template("register.html", error="Email déjà utilisé."), 409

    pw_hash = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())

    user = User(
        email=email,
        password_hash=pw_hash,
        role="user",
        is_approved=False
    )

    db.session.add(user)
    db.session.commit()

    return render_template(
        "login.html",
        error="Compte créé. En attente de validation par l’administrateur."
    ), 201


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")

    email = request.form.get("email", "").strip().lower()
    password = request.form.get("password", "")

    u = User.query.filter_by(email=email).first()

    if not u or not u.check_password(password):
        return render_template("login.html", error="Identifiants invalides."), 401

    session["user_id"] = u.id

    if u.role == "admin":
        return redirect(url_for("admin_panel"))

    if not u.is_approved:
        return render_template(
            "login.html",
            error="Compte en attente de validation par un administrateur."
        ), 403

    return redirect(url_for("concessionnaires"))


@app.get("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))


@app.get("/concessionnaires")
@login_required
def concessionnaires():
    return render_template("concessionnaires.html")


@app.get("/admin")
@admin_required
def admin_panel():
    pending = User.query.filter_by(role="user", is_approved=False).all()
    approved = User.query.filter_by(role="user", is_approved=True).all()
    return render_template("admin.html", pending=pending, approved=approved)


@app.post("/admin/approve/<int:user_id>")
@admin_required
def admin_approve(user_id):
    u = db.session.get(User, user_id)
    if u and u.role == "user":
        u.is_approved = True
        db.session.commit()
    return redirect(url_for("admin_panel"))


@app.post("/admin/revoke/<int:user_id>")
@admin_required
def admin_revoke(user_id):
    u = db.session.get(User, user_id)
    if u and u.role == "user":
        u.is_approved = False
        db.session.commit()
    return redirect(url_for("admin_panel"))


@app.post("/admin/delete/<int:user_id>")
@admin_required
def admin_delete(user_id):
    u = db.session.get(User, user_id)
    if u and u.role == "user":
        db.session.delete(u)
        db.session.commit()
    return redirect(url_for("admin_panel"))


# =========================
# DOC API (ADMIN ONLY)
# =========================
@app.get("/api/docs")
@admin_required
def api_docs():
    return render_template("api_docs.html")


# =========================
# API REST
# =========================
@app.post("/api/predict")
@login_required
def predict():
    data = request.get_json(silent=True) or {}

    required = ["brand", "model", "fuel", "gearbox", "year", "mileage_km"]
    missing = [k for k in required if k not in data]
    if missing:
        return jsonify(error="validation_error", details=f"Missing fields: {missing}"), 422

    try:
        year = int(data["year"])
        km = int(data["mileage_km"])
    except Exception:
        return jsonify(error="validation_error", details="year and mileage_km must be integers"), 422

    # MOCK modèle
    base = 12000
    price = base + (year - 2015) * 700 - (km / 1000) * 120
    price = max(800, round(price, 0))

    return jsonify(predicted_price_eur=price), 200


@app.get("/api/market/price-series")
@login_required
def market_price_series():
    marque = request.args.get("marque")
    annee = request.args.get("annee")
    carburant = request.args.get("carburant")

    if not (marque and annee and carburant):
        return jsonify(error="validation_error",
                       details="Paramètres requis: marque, annee, carburant"), 422

    x = ["Jan", "Feb", "Mar", "Apr", "May", "Jun"]
    y = [12000, 11800, 12100, 12500, 12300, 12700]

    return jsonify(filters={"marque": marque, "annee": annee, "carburant": carburant},
                   x=x, y=y), 200


@app.get("/api/market/top-change")
@login_required
def market_top_change():
    marque = request.args.get("marque")
    carburant = request.args.get("carburant")

    if not (marque and carburant):
        return jsonify(error="validation_error",
                       details="Paramètres requis: marque, carburant"), 422

    return jsonify(filters={"marque": marque, "carburant": carburant},
                   year=2022,
                   change_eur=1800), 200


# =========================
# LANCEMENT
# =========================
if __name__ == "__main__":
    app.run(debug=True)
