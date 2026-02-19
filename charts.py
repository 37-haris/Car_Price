from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
import chart_query as chart_queries
from database import get_db
from chart_query import brands_per_year

router = APIRouter()

# ✅ Endpoint for your card
@router.get("/total-cars")
def get_total_cars(db: Session = Depends(get_db)):
    total = chart_queries.total_cars(db)
    return {"total": total}

@router.get("/fuel-types")
def get_fuel_types(db: Session = Depends(get_db)):
    return chart_queries.fuel_type_count(db)

@router.get("/count-brands")
def get_count_brands(db: Session = Depends(get_db)):
    return chart_queries.count_brands(db)

@router.get("/count-models")
def get_count_models(db: Session = Depends(get_db)):
    return chart_queries.count_models(db)
# @router.get("/models-per-year")
# def get_models_per_year(db: Session = Depends(get_db)):
#     return models_per_year(db)

@router.get("/brands-per-year")
def get_brands_per_year(db: Session = Depends(get_db)):
    return brands_per_year(db)