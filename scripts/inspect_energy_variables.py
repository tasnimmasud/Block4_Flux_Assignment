import pandas as pd
from pathlib import Path

file_path = Path(
    "data/processed/prepared/CZ-Stn_prepared.csv"
)

# Read column names only; do not load the full dataset
columns = pd.read_csv(file_path, nrows=0).columns

print("\nENERGY-BALANCE RELATED VARIABLES")
print("=" * 60)

keywords = [
    "NETRAD",
    "SW_IN",
    "SW_OUT",
    "LW_IN",
    "LW_OUT",
    "G_F",
    "G",
    "H_F",
    "LE_F",
]

for keyword in keywords:

    matches = [
        column for column in columns
        if keyword in column
    ]

    print(f"\n{keyword}:")
    if matches:
        for column in matches:
            print(f"  {column}")
    else:
        print("  No matching columns found")