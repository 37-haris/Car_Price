from sqlalchemy.orm import Session
from sqlalchemy import text

from database import get_db

def cars_by_transmission(db: Session):
    query = text("""
        SELECT Transmission AS label, COUNT(*) AS value
        FROM info
        GROUP BY Transmission
    """)
    result = db.execute(query).fetchall()
    return [{"label": row.label, "value": row.value} for row in result]
def total_cars(db: Session):
    data = cars_by_transmission(db)
    return sum(item["value"] for item in data)


def fuel_type_count(db: Session):
    query = text("""
        SELECT COUNT(DISTINCT Fuel_Type) AS total
        FROM info
    """)
    result = db.execute(query).fetchone()  # returns tuple like (3,)
    
    total = result[0] if result and result[0] is not None else 0
    return {"total": total}


def count_brands(db: Session):
    query = text("""
        SELECT 
            COUNT(DISTINCT SUBSTRING_INDEX(Name, ' ', 1)) AS brand_count
        FROM info
    """)
    result = db.execute(query).fetchone()
    return {
        "brand_count": result[0]  # this will now be a number
    }

def count_models(db: Session):
    query = text("""
        SELECT 
            COUNT(DISTINCT SUBSTRING(Name, LOCATE(' ', Name) + 1)) AS model_count
        FROM info
    """)
    result = db.execute(query).fetchone()
    return {
        "model_count": result[0]
    }

def brands_per_year(db: Session):
    query = text("""
        SELECT 
            Year,
            SUBSTRING_INDEX(Name, ' ', 1) AS brand
        FROM info
        WHERE Name IS NOT NULL
        ORDER BY Year
    """)
    result = db.execute(query).fetchall()
    return [
        {"year": row.Year, "brand": row.brand}
        for row in result
        if row.brand is not None
    ]














def avg_price_by_fuel(db: Session):
    query = text("""
        SELECT Fuel_Type AS label, AVG(Price) AS value
        FROM info
        GROUP BY Fuel_Type
    """)
    result = db.execute(query).fetchall()
    return [{"label": row.label, "value": float(row.value)} for row in result]

def all_charts(db: Session):
    return {
        "fuel_price": avg_price_by_fuel(db),
        "transmission": cars_by_transmission(db),
        "power": fuel_type_count(db)
    }