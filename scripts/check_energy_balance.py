import pandas as pd
import zipfile
from pathlib import Path
from io import BytesIO

# --------------------------------------------------
# 1. Locate the original CZ-Stn ZIP archive
# --------------------------------------------------

zip_files = list(Path("data/raw").glob("*CZ-Stn*.zip"))

if len(zip_files) != 1:
    raise RuntimeError(
        f"Expected one CZ-Stn ZIP file, found {len(zip_files)}"
    )

zip_path = zip_files[0]

# --------------------------------------------------
# 2. Find the variable description file in the ZIP
# --------------------------------------------------

print("\nENERGY VARIABLE DEFINITIONS")
print("=" * 70)

with zipfile.ZipFile(zip_path, "r") as archive:

    metadata_files = [
        name for name in archive.namelist()
        if "BIFVARINFO" in name.upper()
        and "HH" in name.upper()
        and name.lower().endswith(".csv")
    ]

    if not metadata_files:
        raise RuntimeError(
            "Could not find the half-hourly BIFVARINFO CSV."
        )

    metadata_name = metadata_files[0]

    with archive.open(metadata_name) as metadata_file:
        metadata = pd.read_csv(metadata_file)

    # Find the column containing variable names
    variable_column = next(
        (
            col for col in metadata.columns
            if "VARIABLE" in col.upper()
        ),
        None
    )

    if variable_column is None:
        raise RuntimeError(
            "Could not identify the variable-name column. "
            f"Available columns: {list(metadata.columns)}"
        )

    selected_variables = [
        "NETRAD",
        "G_F_MDS",
        "H_F_MDS",
        "LE_F_MDS",
    ]

    matches = metadata[
        metadata[variable_column].astype(str).isin(
            selected_variables
        )
    ]

    print(f"Metadata file: {metadata_name}")
    print("\nMatching metadata rows:")

    print(matches.to_string(index=False))

# --------------------------------------------------
# 3. Check data availability in prepared data
# --------------------------------------------------

print("\n\nENERGY VARIABLE DATA COVERAGE")
print("=" * 70)

prepared_file = Path(
    "data/processed/prepared/CZ-Stn_prepared.csv"
)

variables = [
    "NETRAD",
    "G_F_MDS",
    "H_F_MDS",
    "LE_F_MDS",
]

df = pd.read_csv(
    prepared_file,
    usecols=variables
)

for variable in variables:

    values = pd.to_numeric(
        df[variable],
        errors="coerce"
    )

    print(f"\n{variable}")
    print(f"Valid records: {values.notna().sum():,}")
    print(f"Missing records: {values.isna().sum():,}")
    print(f"Missing percentage: {values.isna().mean() * 100:.2f}%")
    print(f"Minimum: {values.min()}")
    print(f"Maximum: {values.max()}")

print("\nENERGY-BALANCE VERIFICATION COMPLETED")