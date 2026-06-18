import pandas as pd

df = pd.read_csv("data/raw/yellow_tripdata_2019-01.csv")

print("=== Shape ===")
print(df.shape)

print("\n=== Column Types ===")
print(df.dtypes)

print("\n=== Stats ===")
print(df.describe())

print("\n=== Missing values ===")
print(df.isnull().sum())