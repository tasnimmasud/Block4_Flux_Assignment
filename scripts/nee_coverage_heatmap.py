
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

# Project folders
input_folder = Path("data/processed/prepared")
figure_folder = Path("output/figures")
table_folder = Path("output/tables")

figure_folder.mkdir(parents=True, exist_ok=True)
table_folder.mkdir(parents=True, exist_ok=True)

# Find the five prepared datasets
files = sorted(input_folder.glob("*_prepared.csv"))

if len(files) != 5:
    raise RuntimeError(
        f"Expected 5 prepared files, found {len(files)}"
    )

all_results = []

# Process each site
for file_path in files:
    print(f"\nProcessing {file_path.name}")

    df = pd.read_csv(
        file_path,
        usecols=[
            "TIMESTAMP_START",
            "SITE_ID",
            "NEE_CUT_REF",
            "NEE_CUT_REF_QC",
        ],
        parse_dates=["TIMESTAMP_START"],
    )

    # Extract calendar year
    df["YEAR"] = df["TIMESTAMP_START"].dt.year

    # Measured NEE = valid NEE value and QC equal to zero
    df["MEASURED_NEE"] = (
        df["NEE_CUT_REF"].notna()
        & (df["NEE_CUT_REF_QC"] == 0)
    )

    # Calculate annual coverage
    yearly = (
        df.groupby(["SITE_ID", "YEAR"])
        .agg(
            total_records=("MEASURED_NEE", "size"),
            measured_records=("MEASURED_NEE", "sum"),
        )
        .reset_index()
    )

    yearly["measured_nee_percent"] = (
        yearly["measured_records"]
        / yearly["total_records"]
        * 100
    )

    all_results.append(yearly)

# Combine all five sites
coverage = pd.concat(all_results, ignore_index=True)

# Save numerical results
coverage.to_csv(
    table_folder / "annual_nee_coverage.csv",
    index=False,
)

# Create site-by-year table for heatmap
heatmap_data = coverage.pivot(
    index="SITE_ID",
    columns="YEAR",
    values="measured_nee_percent",
)

# Arrange sites consistently
site_order = ["CZ-Stn", "IT-TrF", "NZ-ADw", "US-UiC", "CN-YaS"]
heatmap_data = heatmap_data.reindex(site_order)

# Draw heatmap
fig, ax = plt.subplots(figsize=(15, 5))

image = ax.imshow(
    heatmap_data,
    aspect="auto",
    cmap="YlGnBu",
    vmin=0,
    vmax=100,
)

ax.set_xticks(range(len(heatmap_data.columns)))
ax.set_xticklabels(heatmap_data.columns, rotation=45)

ax.set_yticks(range(len(heatmap_data.index)))
ax.set_yticklabels(heatmap_data.index)

ax.set_xlabel("Year")
ax.set_ylabel("FLUXNET site")
ax.set_title("Annual measured NEE coverage (QC = 0)")

# Display percentages inside the heatmap
for row in range(len(heatmap_data.index)):
    for col in range(len(heatmap_data.columns)):
        value = heatmap_data.iloc[row, col]

        if pd.notna(value):
            ax.text(
                col,
                row,
                f"{value:.1f}",
                ha="center",
                va="center",
                fontsize=7,
            )

colorbar = fig.colorbar(image, ax=ax)
colorbar.set_label("Measured NEE observations (%)")

fig.tight_layout()

# Save figure
figure_path = (
    figure_folder / "annual_nee_coverage_heatmap.png"
)

fig.savefig(
    figure_path,
    dpi=300,
    bbox_inches="tight",
)

plt.close(fig)

# Print results
print("\nANNUAL NEE COVERAGE")
print(coverage.to_string(index=False))

print("\nTable saved:", table_folder / "annual_nee_coverage.csv")
print("Heatmap saved:", figure_path)
print("\nHEATMAP CREATED SUCCESSFULLY")
