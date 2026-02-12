from flask import Flask, request, jsonify, render_template, redirect, url_for, session
from functools import wraps

app = Flask(__name__)
app.secret_key = "dev-secret-change-me"  # ok pour soutenance, change en prod

# --- Auth ultra simple (pour soutenir "login") ---
USERS = {"admin@demo.com": "demo123"}  # hardcodé = suffisant pour livrable

def login_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        if not session.get("user"):
            return redirect(url_for("login"))
        return fn(*args, **kwargs)
    return wrapper


# --- PAGES ---
@app.get("/")
def home():
    return render_template("index.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")

    email = request.form.get("email", "").strip()
    password = request.form.get("password", "")

    if USERS.get(email) == password:
        session["user"] = email
        return redirect(url_for("concessionnaires"))

    # simple: on renvoie la page avec un message (à afficher si tu veux)
    return render_template("login.html", error="Identifiants invalides"), 401

@app.get("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))

@app.get("/concessionnaires")
@login_required
def concessionnaires():
    return render_template("concessionnaires.html")

@app.get("/api/docs")
def api_docs():
    return render_template("api_docs.html")


# --- API REST ---
@app.get("/api/health")
def health():
    return jsonify(status="ok")

@app.post("/api/predict")
@login_required
def predict():
    """
    Attendu: JSON { feature1: ..., feature2: ... }
    Retour: { predicted_price: float }
    """
    data = request.get_json(silent=True) or {}

    # TODO: ici tu chargeras ton modèle + preprocess (pkl) et tu feras predict
    # Pour livrable immédiat: on met une "fausse" prédiction cohérente.
    try:
        annee = int(data.get("annee"))
        km = int(data.get("kilometrage"))
    except Exception:
        return jsonify(
            error="BadRequest",
            message="Champs manquants ou invalides (annee, kilometrage)."
        ), 400

    # Démo: prix qui baisse avec km, monte avec année (bidon mais stable)
    base = 12000
    price = base + (annee - 2015) * 700 - (km / 1000) * 120
    price = max(800, round(price, 0))

    return jsonify(predicted_price=price)

@app.get("/api/market/price-series")
@login_required
def market_price_series():
    """
    Query params:
      - marque
      - annee
      - carburant
    Retour: { x: [...], y: [...] }
    """
    marque = request.args.get("marque")
    annee = request.args.get("annee")
    carburant = request.args.get("carburant")
    if not (marque and annee and carburant):
        return jsonify(
            error="BadRequest",
            message="Paramètres requis: marque, annee, carburant."
        ), 400

    # TODO: calcul réel depuis ton CSV clean
    # Démo: une série fictive
    x = ["Jan", "Feb", "Mar", "Apr", "May", "Jun"]
    y = [12000, 11800, 12100, 12500, 12300, 12700]
    return jsonify(x=x, y=y, marque=marque, annee=annee, carburant=carburant)

@app.get("/api/market/top-change")
@login_required
def market_top_change():
    """
    Query params:
      - marque
      - carburant
    Retour: { year: 2022, change: 1800 }
    """
    marque = request.args.get("marque")
    carburant = request.args.get("carburant")
    if not (marque and carburant):
        return jsonify(
            error="BadRequest",
            message="Paramètres requis: marque, carburant."
        ), 400

    # TODO: calcul réel
    return jsonify(year=2022, change=1800, marque=marque, carburant=carburant)


if __name__ == "__main__":
    app.run(debug=True)
