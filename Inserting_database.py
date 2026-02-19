import pandas as pd
from sqlalchemy import create_engine, text

# Database connection
engine = create_engine("mysql+pymysql://root:@localhost/car")

# Create table if not exists
with engine.connect() as conn:
    conn.execute(text("""
        CREATE TABLE IF NOT EXISTS info (
            id INT AUTO_INCREMENT PRIMARY KEY,
            Name VARCHAR(255),
            Location VARCHAR(100),
            Year INT,
            Kilometers_Driven INT,
            Fuel_Type VARCHAR(50),
            Transmission VARCHAR(50),
            Owner_Type VARCHAR(50),
            Mileage VARCHAR(50),
            Engine VARCHAR(50),
            Power VARCHAR(50),
            Seats FLOAT,
            New_Price VARCHAR(50),
            Price FLOAT
        )
    """))
    conn.commit()

# Read CSV
df = pd.read_csv(r"Data\train.csv")

# Clean column names (remove spaces)
df.columns = df.columns.str.strip()

# Insert into MySQL
df.to_sql("info", con=engine, if_exists="append", index=False)

print(f"Done! {len(df)} rows inserted.")