
import pandas as pd
from pathlib import Path

# Project folders
input_folder = Path("data/processed")
output_folder = Path("data/processed/prepared")

output_folder.mkdir(parents=True, exist_ok=True)

# Map filenames to site identifiers
site_ids = {
    "AMF_US-UiC": "US-UiC",
    "CNF_CN-YaS": "CN-YaS",
    "EUF_CZ-Stn": "CZ-Stn",
    "ICOS_IT-TrF": "IT-TrF",
    "TERN_NZ-ADw": "NZ-ADw",
}

files = sorted(input_folder.glob("*FLUXMET_HH_*.csv"))

if len(files) != 5:
    raise RuntimeError(
        f"Expected 5 input CSV files, found {len(files)}."
    )

for file_path in files:
    print(f"\nPreparing {file_path.name}")

    # Identify site
    site_id = next(
        (
            site for prefix, site in site_ids.items()
            if file_path.name.startswith(prefix)
        ),
        None
    )

    if site_id is None:
        raise ValueError(f"Unknown site: {file_path.name}")

    # Read CSV; interpret -9999 as missing
    df = pd.read_csv(
        file_path,
        na_values=[-9999, "-9999"]
    )

    # Parse timestamps
    df["TIMESTAMP_START"] = pd.to_datetime(
        df["TIMESTAMP_START"].astype("string"),
        format="%Y%m%d%H%M",
        errors="coerce"
    )

    df["TIMESTAMP_END"] = pd.to_datetime(
        df["TIMESTAMP_END"].astype("string"),
        format="%Y%m%d%H%M",
        errors="coerce"
    )

    # Add site identifier
    df["SITE_ID"] = site_id

    # Check timestamp parsing
    invalid_timestamps = df["TIMESTAMP_START"].isna().sum()

    if invalid_timestamps > 0:
        raise ValueError(
            f"{site_id}: {invalid_timestamps} invalid start timestamps."
        )

    # Save prepared data
    output_path = output_folder / f"{site_id}_prepared.csv"

    df.to_csv(output_path, index=False)

    print(f"Site: {site_id}")
    print(f"Rows: {len(df):,}")
    print(f"Columns: {len(df.columns)}")
    print(f"Missing values: {df.isna().sum().sum():,}")
    print(f"Saved: {output_path}")

print("\nALL FIVE DATASETS PREPARED SUCCESSFULLY")
