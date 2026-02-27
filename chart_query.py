from sqlalchemy.orm import Session
from sqlalchemy import text

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


def brands_per_model(db: Session):
    query = text("""
        SELECT 
            SUBSTRING_INDEX(Name, ' ', 1) AS brand,
            COUNT(*) as count
        FROM info
        WHERE Name IS NOT NULL
        GROUP BY brand
        ORDER BY count DESC
        LIMIT 30
        
    """)
    result = db.execute(query).fetchall()
    return [{"model": row.brand, "count": row.count} for row in result]


def owner_type_price(db: Session):
    query = text("""
        SELECT Fuel_Type, ROUND(AVG(Price), 2) as avg_price, 
               ROUND(MIN(Price), 2) as min_price, 
               ROUND(MAX(Price), 2) as max_price
        FROM info
        WHERE Price IS NOT NULL AND Fuel_Type IS NOT NULL
        GROUP BY Fuel_Type
        ORDER BY avg_price DESC
    """)
    result = db.execute(query).fetchall()
    return [{"owner_type": row.Fuel_Type, "avg_price": row.avg_price, 
             "min_price": row.min_price, "max_price": row.max_price} for row in result]


def random_car(db: Session):
    query = text("""
        SELECT Name, Location, Year, Kilometers_Driven, 
               Fuel_Type, Transmission, Owner_Type, Price
        FROM info
        WHERE Price IS NOT NULL AND Name IS NOT NULL
        ORDER BY RAND()
        LIMIT 1
    """)
    result = db.execute(query).fetchone()
    return {
        "name": result.Name,
        "location": result.Location,
        "year": result.Year,
        "km": result.Kilometers_Driven,
        "fuel": result.Fuel_Type,
        "transmission": result.Transmission,
        "owner": result.Owner_Type,
        "price": result.Price
    }
   
   
def biggest_price_evolution(db: Session):
    query = text("""
        SELECT 
            SUBSTRING_INDEX(Name, ' ', 1) AS brand,
            Fuel_Type,
            Year,
            ROUND(AVG(Price), 2) as avg_price
        FROM info
        WHERE Price IS NOT NULL AND Name IS NOT NULL
        GROUP BY brand, Fuel_Type, Year
        ORDER BY brand, Fuel_Type, Year
    """)
    result = db.execute(query).fetchall()

    # Calculate year-over-year evolution per brand+fuel
    grouped = {}
    for row in result:
        key = f"{row.brand} - {row.Fuel_Type}"
        if key not in grouped:
            grouped[key] = []
        grouped[key].append({"year": row.Year, "avg_price": row.avg_price})

    evolutions = []
    for label, points in grouped.items():
        if len(points) >= 2:
            sorted_points = sorted(points, key=lambda x: x["year"])
            max_jump = 0
            best_year = None
            for i in range(1, len(sorted_points)):
                diff = sorted_points[i]["avg_price"] - sorted_points[i-1]["avg_price"]
                if abs(diff) > abs(max_jump):
                    max_jump = diff
                    best_year = sorted_points[i]["year"]
            evolutions.append({
                "label": label,
                "year": best_year,
                "evolution": round(max_jump, 2),
                "data": sorted_points
            })

    # Return top 10 biggest evolutions
    evolutions.sort(key=lambda x: abs(x["evolution"]), reverse=True)
    return evolutions[:10]

def price_evolution(db: Session):
    query = text("""
        SELECT 
            SUBSTRING_INDEX(Name, ' ', 1) AS brand,
            Year,
            ROUND(AVG(Price), 2) as avg_price
        FROM info
        WHERE Price IS NOT NULL AND Name IS NOT NULL
        GROUP BY brand, Year, Fuel_Type
        ORDER BY Year
    """)
    result = db.execute(query).fetchall()
    grouped = {}
    for row in result:
        key = f"{row.brand}"
        if key not in grouped:
            grouped[key] = []
        grouped[key].append({"year": row.Year, "avg_price": row.avg_price})
    return [{"label": k, "data": v} for k, v in grouped.items()]


def transmission_distribution(db: Session):
    query = text("""
        SELECT Transmission, COUNT(*) as count
        FROM info
        WHERE Transmission IS NOT NULL
        GROUP BY Transmission
    """)
    result = db.execute(query).fetchall()
    total = sum(row.count for row in result)
    return [{"label": row.Transmission, "count": row.count, 
             "percent": round((row.count / total) * 100, 1)} for row in result]
    
def get_location_insights(db):
    query = text("""
        SELECT 
            Location,
            COUNT(*) as total_cars,
            AVG(Price) as avg_price
        FROM info
        WHERE Price IS NOT NULL AND Location IS NOT NULL
        GROUP BY Location
    """)

    results = db.execute(query).fetchall()

    # Convert to list of dicts
    data = [dict(row._mapping) for row in results]

    # 🔥 Compute insights
    top_city = max(data, key=lambda x: x['total_cars'])
    cheapest_city = min(data, key=lambda x: x['avg_price'])

    return {
        "cities": data,
        "top_city": top_city,
        "cheapest_city": cheapest_city
    }
    
    

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