from contextlib import asynccontextmanager
from fastapi import FastAPI
import joblib as jbl
from pydantic import BaseModel
import pandas as pd


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
    Power: float
    Seats: int
    Consumation: float
    car_age: float
    km_age: float


@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.ml_models = jbl.load("test_model.pkl")
    yield
    app.state.ml_models = None


app = FastAPI(lifespan=lifespan)


@app.post("/predict")
async def predict(body: Body):
    deff = pd.DataFrame([body.model_dump()])    
    result = app.state.ml_models.predict(deff)[0]
    return {"result": result}

