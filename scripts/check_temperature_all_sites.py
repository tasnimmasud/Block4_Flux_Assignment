
import pandas as pd
from pathlib import Path

folder = Path("data/processed/prepared")

files = sorted(folder.glob("*_prepared.csv"))

results = []

for file_path in files:
    print(f"\nChecking {file_path.name}")

    df = pd.read_csv(
        file_path,
        usecols=["TIMESTAMP_START", "TA_F", "TA_F_QC"],
        na_values=[-9999, "-9999"]
    )

    df["TIMESTAMP_START"] = pd.to_datetime(
        df["TIMESTAMP_START"],
        errors="coerce"
    )

    df["YEAR"] = df["TIMESTAMP_START"].dt.year

    site_id = file_path.stem.replace("_prepared", "")

    for year, group in df.groupby("YEAR"):
        results.append({
            "SITE_ID": site_id,
            "YEAR": year,
            "TA_F_available_percent": (
                group["TA_F"].notna().mean() * 100
            ),
            "TA_F_QC_available_percent": (
                group["TA_F_QC"].notna().mean() * 100
            )
        })

result_df = pd.DataFrame(results)

print("\n" + "=" * 70)
print("TA_F AVAILABILITY ACROSS ALL FIVE SITES")
print("=" * 70)

print(
    result_df.to_string(
        index=False,
        formatters={
            "TA_F_available_percent": "{:.2f}%".format,
            "TA_F_QC_available_percent": "{:.2f}%".format
        }
    )
)

output_folder = Path("output/tables")
output_folder.mkdir(parents=True, exist_ok=True)

result_df.to_csv(
    output_folder / "temperature_availability_all_sites.csv",
    index=False
)

print("\nReport saved to output/tables/temperature_availability_all_sites.csv")
