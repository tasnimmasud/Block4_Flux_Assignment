
import pandas as pd
from pathlib import Path

data_folder = Path("data/processed/prepared")
output_folder = Path("output/tables")
output_folder.mkdir(parents=True, exist_ok=True)

files = sorted(data_folder.glob("*_prepared.csv"))

if len(files) != 5:
    raise RuntimeError(f"Expected 5 prepared files, found {len(files)}")

variables = [
    "TA_F_MDS",
    "SW_IN_F_MDS",
    "VPD_F_MDS",
    "P_F",
    "NEE_CUT_REF",
    "NEE_CUT_REF_QC",
    "GPP_NT_CUT_REF",
    "RECO_NT_CUT_REF",
    "H_F_MDS",
    "LE_F_MDS",
]

reports = []

for file_path in files:
    print(f"\nChecking {file_path.name}")

    df = pd.read_csv(
        file_path,
        usecols=["TIMESTAMP_START", "TIMESTAMP_END", "SITE_ID"] + variables,
        parse_dates=["TIMESTAMP_START", "TIMESTAMP_END"],
    )

    site_id = df["SITE_ID"].iloc[0]

    start = df["TIMESTAMP_START"].min()
    end = df["TIMESTAMP_START"].max()

    # NEE observations with QC = 0 are measured observations
    measured_nee = (
        df["NEE_CUT_REF"].notna()
        & (df["NEE_CUT_REF_QC"] == 0)
    )

    reports.append({
        "SITE_ID": site_id,
        "Rows": len(df),
        "First timestamp": start,
        "Last timestamp": end,
        "Years covered": df["TIMESTAMP_START"].dt.year.nunique(),
        "Missing NEE (%)": round(
            df["NEE_CUT_REF"].isna().mean() * 100, 2
        ),
        "Measured NEE QC=0 (%)": round(
            measured_nee.mean() * 100, 2
        ),
        "Missing TA (%)": round(
            df["TA_F_MDS"].isna().mean() * 100, 2
        ),
        "Missing SW_IN (%)": round(
            df["SW_IN_F_MDS"].isna().mean() * 100, 2
        ),
    })

report = pd.DataFrame(reports)

print("\n" + "=" * 70)
print("DATA QUALITY SUMMARY")
print("=" * 70)
print(report.to_string(index=False))

output_path = output_folder / "data_quality_summary.csv"
report.to_csv(output_path, index=False)

print(f"\nReport saved to: {output_path}")
