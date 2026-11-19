import pandas as pd
import zipfile
from pathlib import Path

zip_files = list(Path("data/raw").glob("*CZ-Stn*.zip"))

if len(zip_files) != 1:
    raise RuntimeError("Could not identify one CZ-Stn ZIP file.")

with zipfile.ZipFile(zip_files[0], "r") as archive:

    metadata_files = [
        name for name in archive.namelist()
        if "BIFVARINFO" in name.upper()
        and "HH" in name.upper()
        and name.lower().endswith(".csv")
    ]

    metadata_name = metadata_files[0]

    with archive.open(metadata_name) as f:
        metadata = pd.read_csv(f)

print("\nMETADATA COLUMNS")
print(metadata.columns.tolist())

print("\nFIRST 15 METADATA ROWS")
print(metadata.head(15).to_string(index=False))

print("\nSEARCH FOR ENERGY VARIABLE NAMES")
print("=" * 65)

names = ["NETRAD", "G_F_MDS", "H_F_MDS", "LE_F_MDS"]

for name in names:

    matches = metadata[
        metadata.astype(str).apply(
            lambda column: column.str.contains(
                name,
                case=False,
                regex=False
            )
        ).any(axis=1)
    ]

    print(f"\n{name}:")
    if matches.empty:
        print("No matching rows found.")
    else:
        print(matches.to_string(index=False))