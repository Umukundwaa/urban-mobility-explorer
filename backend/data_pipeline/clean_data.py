import pandas as pd
import os

# Load raw data
df = pd.read_csv("data/raw/yellow_tripdata_2019-01.csv")
zones = pd.read_csv("data/raw/taxi_zone_lookup.csv")

# Convert timestamps from text to real datetime objects
df["tpep_pickup_datetime"] = pd.to_datetime(df["tpep_pickup_datetime"])
df["tpep_dropoff_datetime"] = pd.to_datetime(df["tpep_dropoff_datetime"])

# Track excluded rows
excluded_rows = []

# Remove trips with 0 passengers
mask = df["passenger_count"] == 0
excluded_rows.append(df[mask].assign(reason="passenger_count is 0"))
df = df[~mask]

# Remove impossible distances
mask = (df["trip_distance"] <= 0) | (df["trip_distance"] > 100)
excluded_rows.append(df[mask].assign(reason="trip_distance out of range"))
df = df[~mask]

# Remove negative fares
mask = df["fare_amount"] <= 0
excluded_rows.append(df[mask].assign(reason="fare_amount is negative or zero"))
df = df[~mask]

# Remove negative total amount
mask = df["total_amount"] <= 0
excluded_rows.append(df[mask].assign(reason="total_amount is negative or zero"))
df = df[~mask]

# Remove invalid RatecodeID
mask = ~df["RatecodeID"].isin([1, 2, 3, 4, 5, 6])
excluded_rows.append(df[mask].assign(reason="invalid RatecodeID"))
df = df[~mask]

# Fill missing congestion_surcharge with 0
df["congestion_surcharge"] = df["congestion_surcharge"].fillna(0)

# Save excluded rows to quality log
excluded_df = pd.concat(excluded_rows)
excluded_df.to_csv("backend/data_pipeline/data_quality_log.csv", index=False)
print(f"Excluded {len(excluded_df)} bad rows")

# trip duration in minutes
df["trip_duration_minutes"] = (
    df["tpep_dropoff_datetime"] - df["tpep_pickup_datetime"]
        ).dt.total_seconds() / 60

# fare per mile
df["fare_per_mile"] = df["fare_amount"] / df["trip_distance"]

# time of day bucket
def get_time_of_day(hour):
    if 6 <= hour < 10:
        return "morning_rush"
    elif 10 <= hour < 16:
        return "daytime"
    elif 16 <= hour < 20:
        return "evening_rush"
    else:
        return "night"

df["time_of_day"] = df["tpep_pickup_datetime"].dt.hour.apply(get_time_of_day)

# Merge with zone names for pickup location
df = df.merge(zones, left_on="PULocationID", right_on="LocationID", how="left")
df = df.rename(columns={"Borough": "pickup_borough", "Zone": "pickup_zone"})
df = df.drop(columns=["LocationID", "service_zone"])

# Merge with zone names for dropoff location
df = df.merge(zones, left_on="DOLocationID", right_on="LocationID", how="left")
df = df.rename(columns={"Borough": "dropoff_borough", "Zone": "dropoff_zone"})
df = df.drop(columns=["LocationID", "service_zone"])

# Save cleaned data
os.makedirs("data/sample", exist_ok=True)
df.to_csv("data/sample/cleaned_trips.csv", index=False)
print(f"Cleaned data saved: {len(df)} rows remaining")