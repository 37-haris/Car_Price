from fastapi import FastAPI, Request, Form, Depends, HTTPException
from contextlib import asynccontextmanager
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker, declarative_base, Session
from passlib.context import CryptContext
from itsdangerous import URLSafeSerializer
from starlette.middleware.base import BaseHTTPMiddleware
import charts
import joblib as jbl
import pandas as pd

# App Setup
@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.ml_models = jbl.load("model.pkl")
    print("Model loaded successfully")
    yield
    app.state.ml_models = None
    print("Model unloaded successfully")
app = FastAPI(lifespan=lifespan)

app.mount("/static", StaticFiles(directory="template/static"), name="static")
app.include_router(charts.router, prefix="/charts", tags=["Charts"])
templates = Jinja2Templates(directory="template")

# Database
DATABASE_URL = "mysql+pymysql://root:@localhost/car"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()

num= ['Year', 'Kilometers_Driven', 'Consommation', 'Engine']
cat = ['Location', 'Fuel_Type', 'Transmission', 'Owner_Type', 'Brand',
       'Model']

class Body(BaseModel):
    Fuel_Type: str
    Transmission: str
    Owner_Type: str
    Location: str
    Brand: str
    Model: str
    Year: int
    Kilometers_Driven: float
    Engine: float
    Consommation: float
    
    


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(150), unique=True)
    email = Column(String(150), unique=True)
    password = Column(String(255))
    role = Column(String(50), default="user")

Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Security
pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")
serializer = URLSafeSerializer("supersecretkey")

# Middleware
class AuthMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        public_paths = ["/login", "/register", "/static"]
        if any(request.url.path.startswith(path) for path in public_paths):
            return await call_next(request)

        token = request.cookies.get("session")
        if not token:
            return RedirectResponse("/login", status_code=303)

        try:
            email = serializer.loads(token)
        except:
            return RedirectResponse("/login", status_code=303)

        db = SessionLocal()
        try:
            user = db.query(User).filter(User.email == email).first()
        finally:
            db.close()

        if not user:
            return RedirectResponse("/login", status_code=303)

        request.state.user = user
        request.state.role = user.role
        return await call_next(request)

app.add_middleware(AuthMiddleware)

# Routes
@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    user = getattr(request.state, "user", None)
    role = getattr(request.state, "role", None)
    if not user:
        return RedirectResponse("/login", status_code=303)
    response = templates.TemplateResponse("index.html", {"request": request, "user": user, "role": role})
    response.headers["Cache-Control"] = "no-store, no-cache, must-revalidate, max-age=0"
    response.headers["Pragma"] = "no-cache"
    response.headers["Expires"] = "0"
    return response

@app.post("/predict")
async def predict(body: Body):
    print(body)
    df = pd.DataFrame([{
        "Brand": body.Brand,
        "Model": body.Model,
        "Fuel_Type": body.Fuel_Type,
        "Transmission": body.Transmission,
        "Year": body.Year,
        "Kilometers_Driven": body.Kilometers_Driven,
        "Engine": body.Engine,
        "Consommation": body.Consommation,
        "Location": body.Location,
        "Owner_Type": body.Owner_Type
    }])
    result = app.state.ml_models.predict(df)[0]
    return {"result": float(result)}

@app.get("/prediction", response_class=HTMLResponse)
def prediction_page(request: Request):
    user = getattr(request.state, "user", None)
    role = getattr(request.state, "role", None)
    if not user:
        return RedirectResponse("/login", status_code=303)
    response = templates.TemplateResponse("prediction.html", {"request": request, "user": user, "role": role})
    response.headers["Cache-Control"] = "no-store, no-cache, must-revalidate, max-age=0"
    response.headers["Pragma"] = "no-cache"
    response.headers["Expires"] = "0"
    return response

@app.get("/user", response_class=HTMLResponse)
def user_page(request: Request):
    user = getattr(request.state, "user", None)
    role = getattr(request.state, "role", None)
    if not user:
        return RedirectResponse("/login", status_code=303)
    response = templates.TemplateResponse("users.html", {"request": request, "user": user, "role": role})
    response.headers["Cache-Control"] = "no-store, no-cache, must-revalidate, max-age=0"
    response.headers["Pragma"] = "no-cache"
    response.headers["Expires"] = "0"
    return response

@app.get("/settings", response_class=HTMLResponse)
def settings_page(request: Request):
    user = getattr(request.state, "user", None)
    role = getattr(request.state, "role", None)
    if not user:
        return RedirectResponse("/login", status_code=303)
    response = templates.TemplateResponse("settings.html", {"request": request, "user": user, "role": role})
    response.headers["Cache-Control"] = "no-store, no-cache, must-revalidate, max-age=0"
    response.headers["Pragma"] = "no-cache"
    response.headers["Expires"] = "0"
    return response

@app.get("/login", response_class=HTMLResponse)
def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@app.post("/register")
def register(name: str = Form(...), email: str = Form(...), password: str = Form(...), db: Session = Depends(get_db)):
    if db.query(User).filter(User.email == email).first():
        raise HTTPException(status_code=400, detail="Email exists")
    hashed = pwd_context.hash(password)
    user = User(name=name, email=email, password=hashed)
    db.add(user)
    db.commit()
    return RedirectResponse("/login", status_code=303)

@app.post("/login")
def login(email: str = Form(...), password: str = Form(...), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == email).first()
    if not user or not pwd_context.verify(password, user.password):
        raise HTTPException(status_code=400, detail="Invalid credentials")
    response = RedirectResponse("/", status_code=303)
    token = serializer.dumps(user.email)
    response.set_cookie("session", token)
    return response

@app.get("/profile", response_class=HTMLResponse)
def profile(request: Request):
    user = getattr(request.state, "user", None)
    if not user:
        return RedirectResponse("/login", status_code=303)
    return f"<h2>Profile Page</h2><p>Name: {user.name}</p><p>Email: {user.email}</p><p>Role: {user.role}</p><a href='/'>Home</a>"

@app.get("/admin")
def admin_page(request: Request):
    user = getattr(request.state, "user", None)
    if not user or user.role != "admin":
        return RedirectResponse("/", status_code=303)
    return {"message": "Welcome Admin 🔥"}

@app.get("/logout")
def logout():
    response = RedirectResponse("/login", status_code=303)
    response.delete_cookie("session")
    return response
