import pandas as pd
import mysql.connector
from dotenv import load_dotenv
import os

load_dotenv("backend/.env")

# Connect to MySQL
conn = mysql.connector.connect(
    host=os.getenv("DB_HOST"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    database=os.getenv("DB_NAME")
)
cursor = conn.cursor()

# Load cleaned data
zones = pd.read_csv("data/raw/taxi_zone_lookup.csv")
trips = pd.read_csv("data/sample/cleaned_trips.csv").head(200000)

# Insert zones first
print("Inserting zones...")
for _, row in zones.iterrows():
    cursor.execute("""
        INSERT IGNORE INTO zones (location_id, borough, zone_name, service_zone)
        VALUES (%s, %s, %s, %s)
    """, (row["LocationID"], row["Borough"], row["Zone"], row["service_zone"]))

conn.commit()
print(f"Zones inserted: {len(zones)} rows")

# Insert trips in batches
print("Inserting trips...")
batch = []
batch_size = 1000
total_inserted = 0

for _, row in trips.iterrows():
    batch.append((
        row["VendorID"], row["tpep_pickup_datetime"], row["tpep_dropoff_datetime"],
        row["passenger_count"], row["trip_distance"], row["RatecodeID"],
        row["PULocationID"], row["DOLocationID"], row["payment_type"],
        row["fare_amount"], row["tip_amount"], row["tolls_amount"],
        row["total_amount"], row["congestion_surcharge"],
        row["trip_duration_minutes"], row["fare_per_mile"], row["time_of_day"]
    ))

    if len(batch) == batch_size:
        cursor.executemany("""
            INSERT INTO trips (
                vendor_id, pickup_datetime, dropoff_datetime,
                passenger_count, trip_distance, rate_code_id,
                pickup_location_id, dropoff_location_id, payment_type,
                fare_amount, tip_amount, tolls_amount,
                total_amount, congestion_surcharge,
                trip_duration_minutes, fare_per_mile, time_of_day
            ) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
        """, batch)
        conn.commit()
        total_inserted += len(batch)
        batch = []
        print(f"  Inserted {total_inserted} rows so far...")

# Insert any remaining rows
if batch:
    cursor.executemany("""
        INSERT INTO trips (
            vendor_id, pickup_datetime, dropoff_datetime,
            passenger_count, trip_distance, rate_code_id,
            pickup_location_id, dropoff_location_id, payment_type,
            fare_amount, tip_amount, tolls_amount,
            total_amount, congestion_surcharge,
            trip_duration_minutes, fare_per_mile, time_of_day
        ) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
    """, batch)
    conn.commit()
    total_inserted += len(batch)

print(f"Trips inserted successfully: {total_inserted} rows")
cursor.close()
conn.close()
print("\n✅ Database fully loaded!")