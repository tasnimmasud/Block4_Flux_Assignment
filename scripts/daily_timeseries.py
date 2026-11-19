import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

# Folders
input_folder = Path("data/processed/prepared")
table_folder = Path("output/tables")
figure_folder = Path("output/figures")

table_folder.mkdir(parents=True, exist_ok=True)
figure_folder.mkdir(parents=True, exist_ok=True)

# Variables for daily time series
variables = [
    "NEE_CUT_REF",
    "GPP_NT_CUT_REF",
    "RECO_NT_CUT_REF",
]

variable_labels = {
    "NEE_CUT_REF": "NEE",
    "GPP_NT_CUT_REF": "GPP (nighttime partitioning)",
    "RECO_NT_CUT_REF": "RECO (nighttime partitioning)",
}

unit = "µmol CO₂ m⁻² s⁻¹"

files = sorted(input_folder.glob("*_prepared.csv"))

if len(files) != 5:
    raise RuntimeError(
        f"Expected 5 prepared files, found {len(files)}"
    )

all_daily_data = []

for file_path in files:

    print(f"\nProcessing {file_path.name}")

    # Read only the columns needed
    columns = ["SITE_ID", "TIMESTAMP_START"] + variables

    df = pd.read_csv(
        file_path,
        usecols=columns
    )

    # Parse timestamps saved in the prepared CSV files
    df["TIMESTAMP_START"] = pd.to_datetime(
        df["TIMESTAMP_START"],
        errors="coerce"
    )

    # Remove rows with invalid timestamps
    df = df.dropna(subset=["TIMESTAMP_START"])

    # Convert measurements to numeric values
    for variable in variables:
        df[variable] = pd.to_numeric(
            df[variable],
            errors="coerce"
        )

    site_id = df["SITE_ID"].iloc[0]

    # Extract calendar date
    df["DATE"] = df["TIMESTAMP_START"].dt.date

    # Calculate daily mean for each variable
    daily = (
        df.groupby(["SITE_ID", "DATE"])[variables]
        .mean()
        .reset_index()
    )

    all_daily_data.append(daily)

    print(f"Site: {site_id}")
    print(f"Daily records: {len(daily):,}")

    # Create a figure with three time-series panels
    fig, axes = plt.subplots(
        3, 1,
        figsize=(13, 10),
        sharex=True
    )

    for ax, variable in zip(axes, variables):

        ax.plot(
            daily["DATE"],
            daily[variable],
            linewidth=0.6
        )

        ax.set_ylabel(f"{variable_labels[variable]}\n({unit})")
        ax.grid(True, alpha=0.3)

    axes[0].set_title(
        f"{site_id}: Daily mean carbon fluxes"
    )

    axes[-1].set_xlabel("Date")

    fig.tight_layout()

    figure_path = (
        figure_folder / f"daily_timeseries_{site_id}.png"
    )

    fig.savefig(
        figure_path,
        dpi=300,
        bbox_inches="tight"
    )

    plt.close(fig)

    print(f"Figure saved: {figure_path}")

# Combine the five sites into one table
combined = pd.concat(
    all_daily_data,
    ignore_index=True
)

combined["DATE"] = pd.to_datetime(combined["DATE"])

combined = combined.sort_values(
    ["SITE_ID", "DATE"]
)

# Save combined daily dataset
output_path = table_folder / "daily_timeseries.csv"

combined.to_csv(
    output_path,
    index=False
)

print("\n" + "=" * 70)
print("DAILY TIME SERIES SUMMARY")
print("=" * 70)

print(
    combined.groupby("SITE_ID")
    .agg(
        first_date=("DATE", "min"),
        last_date=("DATE", "max"),
        daily_records=("DATE", "count")
    )
    .to_string()
)

print(f"\nCombined table saved: {output_path}")
print("\nDAILY TIME SERIES COMPLETED SUCCESSFULLY")