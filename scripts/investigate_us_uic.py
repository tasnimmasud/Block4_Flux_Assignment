
import pandas as pd
from pathlib import Path

file_path = Path(
    "data/processed/prepared/US-UiC_prepared.csv"
)

df = pd.read_csv(
    file_path,
    usecols=[
        "TIMESTAMP_START",
        "NEE_CUT_REF",
        "NEE_CUT_REF_QC",
        "TA_F_MDS",
    ],
)

df["TIMESTAMP_START"] = pd.to_datetime(
    df["TIMESTAMP_START"],
)

# Examine 2022
df_2022 = df[df["TIMESTAMP_START"].dt.year == 2022]

print("\nUS-UiC: 2022 NEE QUALITY CHECK")
print("--------------------------------")

print("\nNumber of records:", len(df_2022))

print("\nNEE quality flag counts:")
print(df_2022["NEE_CUT_REF_QC"].value_counts(dropna=False).sort_index())

print("\nValid NEE values:", df_2022["NEE_CUT_REF"].notna().sum())

print(
    "Measured NEE (QC=0):",
    (
        df_2022["NEE_CUT_REF"].notna()
        & (df_2022["NEE_CUT_REF_QC"] == 0)
    ).sum(),
)

print(
    "Missing air temperature in 2022 (%):",
    round(df_2022["TA_F_MDS"].isna().mean() * 100, 2),
)

# Examine temperature availability across all years
df["YEAR"] = df["TIMESTAMP_START"].dt.year

temperature_check = (
    df.groupby("YEAR")["TA_F_MDS"]
    .apply(lambda x: x.isna().mean() * 100)
)

print("\nUS-UiC: MISSING AIR TEMPERATURE BY YEAR (%)")
print(temperature_check.round(2).to_string())
