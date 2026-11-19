
import pandas as pd
from pathlib import Path

file_path = Path(
    "data/processed/prepared/US-UiC_prepared.csv"
)

# Read column names without loading the full dataset
columns = pd.read_csv(file_path, nrows=0).columns.tolist()

# Find possible temperature and NEE variables
candidates = [
    col for col in columns
    if col.startswith("TA_")
    or col.startswith("NEE_")
]

print("\nAVAILABLE US-UiC TEMPERATURE AND NEE VARIABLES")
print("=" * 65)

for col in candidates:
    print(col)

# Include quality flags and timestamps
usecols = ["TIMESTAMP_START"] + candidates

df = pd.read_csv(
    file_path,
    usecols=usecols,
    parse_dates=["TIMESTAMP_START"],
)

df["YEAR"] = df["TIMESTAMP_START"].dt.year

print("\nYEARLY DATA AVAILABILITY (%)")
print("=" * 65)

for col in candidates:
    yearly_availability = (
        df.groupby("YEAR")[col]
        .apply(lambda x: x.notna().mean() * 100)
    )

    print(f"\n{col}")
    print(yearly_availability.round(1).to_string())

print("\nCHECK COMPLETED")
