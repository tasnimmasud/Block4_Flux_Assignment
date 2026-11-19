import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

# --------------------------------------------------
# 1. Folders
# --------------------------------------------------

input_folder = Path("data/processed/prepared")
table_folder = Path("output/tables")
figure_folder = Path("output/figures")

table_folder.mkdir(parents=True, exist_ok=True)
figure_folder.mkdir(parents=True, exist_ok=True)

# --------------------------------------------------
# 2. Variables
# --------------------------------------------------

variables = [
    "NEE_CUT_REF",
    "LE_F_MDS",
]

variable_labels = {
    "NEE_CUT_REF": "NEE",
    "LE_F_MDS": "Latent heat flux (LE)",
}

units = {
    "NEE_CUT_REF": "µmol CO₂ m⁻² s⁻¹",
    "LE_F_MDS": "W m⁻²",
}

# Northern Hemisphere seasons
northern_seasons = {
    12: "Winter",
    1: "Winter",
    2: "Winter",
    3: "Spring",
    4: "Spring",
    5: "Spring",
    6: "Summer",
    7: "Summer",
    8: "Summer",
    9: "Autumn",
    10: "Autumn",
    11: "Autumn",
}

# Southern Hemisphere seasons
southern_seasons = {
    12: "Summer",
    1: "Summer",
    2: "Summer",
    3: "Autumn",
    4: "Autumn",
    5: "Autumn",
    6: "Winter",
    7: "Winter",
    8: "Winter",
    9: "Spring",
    10: "Spring",
    11: "Spring",
}

season_order = [
    "Spring",
    "Summer",
    "Autumn",
    "Winter",
]

# New Zealand is the only Southern Hemisphere site
southern_hemisphere_sites = ["NZ-ADw"]

# --------------------------------------------------
# 3. Process each site
# --------------------------------------------------

files = sorted(input_folder.glob("*_prepared.csv"))

if len(files) != 5:
    raise RuntimeError(
        f"Expected 5 prepared files, found {len(files)}"
    )

all_results = []

for file_path in files:

    print(f"\nProcessing {file_path.name}")

    columns = [
        "SITE_ID",
        "TIMESTAMP_START",
    ] + variables

    df = pd.read_csv(
        file_path,
        usecols=columns
    )

    # Parse timestamps
    df["TIMESTAMP_START"] = pd.to_datetime(
        df["TIMESTAMP_START"],
        errors="coerce"
    )

    df = df.dropna(
        subset=["TIMESTAMP_START"]
    )

    # Convert variables to numeric
    for variable in variables:
        df[variable] = pd.to_numeric(
            df[variable],
            errors="coerce"
        )

    site_id = df["SITE_ID"].iloc[0]

    # Determine hemisphere
    if site_id in southern_hemisphere_sites:
        hemisphere = "Southern"
        season_mapping = southern_seasons
    else:
        hemisphere = "Northern"
        season_mapping = northern_seasons

    # Extract month and time of day
    df["MONTH"] = df["TIMESTAMP_START"].dt.month

    df["SEASON"] = df["MONTH"].map(
        season_mapping
    )

    df["TIME_MINUTES"] = (
        df["TIMESTAMP_START"].dt.hour * 60
        + df["TIMESTAMP_START"].dt.minute
    )

    # Average observations for each season and
    # half-hour time slot across all available years
    diurnal = (
        df.groupby(
            ["SEASON", "TIME_MINUTES"]
        )[variables]
        .mean()
        .reset_index()
    )

    diurnal["SITE_ID"] = site_id
    diurnal["HEMISPHERE"] = hemisphere

    diurnal["TIME"] = pd.to_datetime(
        diurnal["TIME_MINUTES"],
        unit="m"
    ).dt.strftime("%H:%M")

    all_results.append(diurnal)

    print(f"Site: {site_id}")
    print(f"Hemisphere: {hemisphere}")
    print(f"Diurnal records: {len(diurnal)}")

    # --------------------------------------------------
    # 4. Create seasonal diurnal-cycle figure
    # --------------------------------------------------

    fig, axes = plt.subplots(
        2, 1,
        figsize=(12, 9),
        sharex=True
    )

    for ax, variable in zip(axes, variables):

        for season in season_order:

            season_data = diurnal[
                diurnal["SEASON"] == season
            ].sort_values("TIME_MINUTES")

            if not season_data.empty:

                ax.plot(
                    season_data["TIME_MINUTES"] / 60,
                    season_data[variable],
                    label=season,
                    linewidth=1.5
                )

        ax.set_ylabel(
            f"{variable_labels[variable]}\n"
            f"({units[variable]})"
        )

        ax.grid(True, alpha=0.3)
        ax.legend(title="Season")

    axes[0].set_title(
        f"{site_id}: Seasonal mean diurnal cycles"
    )

    axes[-1].set_xlabel("Time of day (local standard time)")

    axes[-1].set_xticks(
        range(0, 25, 2)
    )

    axes[-1].set_xlim(0, 24)

    fig.tight_layout()

    figure_path = (
        figure_folder
        / f"seasonal_diurnal_{site_id}.png"
    )

    fig.savefig(
        figure_path,
        dpi=300,
        bbox_inches="tight"
    )

    plt.close(fig)

    print(f"Figure saved: {figure_path}")

# --------------------------------------------------
# 5. Combine all sites and save results
# --------------------------------------------------

combined = pd.concat(
    all_results,
    ignore_index=True
)

combined = combined[
    [
        "SITE_ID",
        "HEMISPHERE",
        "SEASON",
        "TIME",
        "TIME_MINUTES",
        "NEE_CUT_REF",
        "LE_F_MDS",
    ]
]

output_path = (
    table_folder / "seasonal_diurnal_cycles.csv"
)

combined.to_csv(
    output_path,
    index=False
)

print("\n" + "=" * 70)
print("SEASONAL DIURNAL CYCLE SUMMARY")
print("=" * 70)

print(
    combined.groupby(
        ["SITE_ID", "SEASON"]
    ).size().unstack(fill_value=0).to_string()
)

print(f"\nCombined table saved: {output_path}")
print("\nSEASONAL DIURNAL CYCLES COMPLETED SUCCESSFULLY")