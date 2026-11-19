import pandas as pd
from pathlib import Path

input_folder = Path("data/processed/prepared")

variables = [
    "NETRAD",
    "G_F_MDS",
    "H_F_MDS",
    "LE_F_MDS",
]

files = sorted(input_folder.glob("*_prepared.csv"))

print("\nENERGY-BALANCE VARIABLE COVERAGE")
print("=" * 75)

results = []

for file_path in files:

    print(f"\nChecking {file_path.name}")

    # Read available column names first
    available_columns = pd.read_csv(
        file_path,
        nrows=0
    ).columns.tolist()

    found_variables = [
        variable for variable in variables
        if variable in available_columns
    ]

    missing_variables = [
        variable for variable in variables
        if variable not in available_columns
    ]

    if missing_variables:
        print("Variables not available:", missing_variables)

    if not found_variables:
        continue

    df = pd.read_csv(
        file_path,
        usecols=found_variables
    )

    site_id = file_path.name.split("_prepared")[0]

    for variable in found_variables:

        values = pd.to_numeric(
            df[variable],
            errors="coerce"
        )

        results.append({
            "SITE_ID": site_id,
            "Variable": variable,
            "Valid_records": values.notna().sum(),
            "Missing_percent": values.isna().mean() * 100,
        })

        print(
            f"{variable}: "
            f"{values.notna().sum():,} valid records, "
            f"{values.isna().mean() * 100:.2f}% missing"
        )

summary = pd.DataFrame(results)

print("\n\nCOVERAGE COMPARISON")
print("=" * 75)

print(
    summary.pivot(
        index="SITE_ID",
        columns="Variable",
        values="Missing_percent"
    ).round(2).to_string()
)

output_path = Path("output/tables/energy_variable_coverage.csv")

output_path.parent.mkdir(parents=True, exist_ok=True)
summary.to_csv(output_path, index=False)

print(f"\nSaved: {output_path}")