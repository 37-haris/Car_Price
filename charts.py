from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
import chart_query as chart_queries
from database import get_db
from chart_query import transmission_distribution, brands_per_model, owner_type_price, random_car, biggest_price_evolution, price_evolution, get_location_insights

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

# @router.get("/brands-per-year")
# def get_brands_with_years(db: Session = Depends(get_db)):
#     return brands_per_year(db)

@router.get("/brands-per-model")
def get_brands_per_model(db: Session = Depends(get_db)):
    return brands_per_model(db)

@router.get("/owner-type-price")
def get_owner_types(db: Session = Depends(get_db)):
    return owner_type_price(db)

@router.get("/random-car")
def get_random_car(db: Session = Depends(get_db)):
    return random_car(db)

@router.get("/biggest-price-evolution")
def get_biggest_price_evolution(db: Session = Depends(get_db)):
    return biggest_price_evolution(db)

@router.get("/price-evolution")
def get_price_evolution(db: Session = Depends(get_db)):
    return price_evolution(db)

@router.get("/transmission")
def get_transmission_distribution(db: Session = Depends(get_db)):
    return transmission_distribution(db)

@router.get("/location-insights")
def location_insights(db: Session = Depends(get_db)):
    return get_location_insights(db)
