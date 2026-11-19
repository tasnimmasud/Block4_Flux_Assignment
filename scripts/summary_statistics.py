import pandas as pd
from pathlib import Path

# Input and output folders
input_folder = Path("data/processed/prepared")
output_folder = Path("output/tables")

output_folder.mkdir(parents=True, exist_ok=True)

# Variables required for the assignment
variables = {
    "TA_F": "Air temperature",
    "SW_IN_F_MDS": "Incoming shortwave radiation",
    "VPD_F_MDS": "Vapour pressure deficit",
    "P_F": "Precipitation",
    "NEE_CUT_REF": "Net ecosystem exchange",
    "GPP_NT_CUT_REF": "Gross primary production",
    "RECO_NT_CUT_REF": "Ecosystem respiration",
    "H_F_MDS": "Sensible heat flux",
    "LE_F_MDS": "Latent heat flux",
}

results = []

files = sorted(input_folder.glob("*_prepared.csv"))

if len(files) != 5:
    raise RuntimeError(
        f"Expected 5 prepared files, found {len(files)}"
    )

for file_path in files:

    print(f"\nProcessing {file_path.name}")

    # Read only the columns needed for this analysis
    columns_to_read = ["SITE_ID"] + list(variables.keys())

    df = pd.read_csv(
        file_path,
        usecols=columns_to_read
    )

    site_id = df["SITE_ID"].iloc[0]

    for variable, description in variables.items():

        values = pd.to_numeric(
            df[variable],
            errors="coerce"
        )

        valid_values = values.dropna()

        if len(valid_values) == 0:
            mean_value = float("nan")
            minimum = float("nan")
            maximum = float("nan")
        else:
            mean_value = valid_values.mean()
            minimum = valid_values.min()
            maximum = valid_values.max()

        missing_percent = values.isna().mean() * 100

        results.append({
            "SITE_ID": site_id,
            "Variable": variable,
            "Description": description,
            "Mean": mean_value,
            "Minimum": minimum,
            "Maximum": maximum,
            "Missing_percent": missing_percent,
            "Valid_records": len(valid_values),
            "Total_records": len(values),
        })

    del df

# Create final results table
summary = pd.DataFrame(results)

# Round numerical results for readability
numeric_columns = [
    "Mean",
    "Minimum",
    "Maximum",
    "Missing_percent",
]

summary[numeric_columns] = summary[numeric_columns].round(3)

# Save CSV
output_path = output_folder / "summary_statistics.csv"

summary.to_csv(output_path, index=False)

print("\n" + "=" * 70)
print("SUMMARY STATISTICS")
print("=" * 70)

print(summary.to_string(index=False))

print(f"\nTable saved to: {output_path}")
print("\nSUMMARY STATISTICS COMPLETED")