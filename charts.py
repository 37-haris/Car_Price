from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
import chart_query as chart_queries
from database import get_db
from chart_query import transmission_distribution, brands_per_model, owner_type_price, random_car, biggest_price_evolution, price_evolution, get_location_insights

router = APIRouter()

# ✅ Endpoint for your card
@router.get("/total-cars", tags=["Charts"], summary='Total Cars')
def get_total_cars(db: Session = Depends(get_db)):
    total = chart_queries.total_cars(db)
    return {"total": total}

@router.get("/fuel-types",tags=["Charts"], summary='Fuel Types Distribution')
def get_fuel_types(db: Session = Depends(get_db)):
    return chart_queries.fuel_type_count(db)

@router.get("/count-brands", tags=["Charts"], summary='Count of Brands')
def get_count_brands(db: Session = Depends(get_db)):
    return chart_queries.count_brands(db)

@router.get("/count-models", tags=["Charts"], summary='Count of Models')
def get_count_models(db: Session = Depends(get_db)):
    return chart_queries.count_models(db)
# @router.get("/models-per-year")
# def get_models_per_year(db: Session = Depends(get_db)):
#     return models_per_year(db)

# @router.get("/brands-per-year")
# def get_brands_with_years(db: Session = Depends(get_db)):
#     return brands_per_year(db)

@router.get("/brands-per-model", tags=["Charts"], summary='Brands Per Model')
def get_brands_per_model(db: Session = Depends(get_db)):
    return brands_per_model(db)

@router.get("/owner-type-price", tags=["Charts"], summary='Owner Type vs Price')
def get_owner_types(db: Session = Depends(get_db)):
    return owner_type_price(db)

@router.get("/random-car" , tags=["Charts"], summary='Random Car Insight')
def get_random_car(db: Session = Depends(get_db)):
    return random_car(db)

@router.get("/biggest-price-evolution", tags=["Charts"], summary='Biggest Price Evolution')
def get_biggest_price_evolution(db: Session = Depends(get_db)):
    return biggest_price_evolution(db)

@router.get("/price-evolution", tags=["Charts"], summary='Price Evolution Over Time')
def get_price_evolution(db: Session = Depends(get_db)):
    return price_evolution(db)

@router.get("/transmission", tags=["Charts"], summary='Transmission Distribution')
def get_transmission_distribution(db: Session = Depends(get_db)):
    return transmission_distribution(db)

@router.get("/location-insights", tags=["Charts"], summary='Location Insights')
def location_insights(db: Session = Depends(get_db)):
    return get_location_insights(db)
