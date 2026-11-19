
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

# Input and output
file_path = Path(
    "data/processed/prepared/IT-TrF_prepared.csv"
)

output_folder = Path("output/figures")
table_folder = Path("output/tables")

output_folder.mkdir(parents=True, exist_ok=True)
table_folder.mkdir(parents=True, exist_ok=True)

# Read energy-balance variables
variables = [
    "NETRAD",
    "G_F_MDS",
    "H_F_MDS",
    "LE_F_MDS",
]

df = pd.read_csv(file_path, usecols=variables)

# Convert to numeric and remove incomplete records
for variable in variables:
    df[variable] = pd.to_numeric(
        df[variable], errors="coerce"
    )

df = df.dropna(subset=variables).copy()

# Calculate energy components (W m-2)
df["Available_energy"] = (
    df["NETRAD"] - df["G_F_MDS"]
)

df["Turbulent_energy"] = (
    df["H_F_MDS"] + df["LE_F_MDS"]
)

# Calculate regression
x = df["Available_energy"].to_numpy()
y = df["Turbulent_energy"].to_numpy()

slope, intercept = np.polyfit(x, y, 1)
correlation = np.corrcoef(x, y)[0, 1]
r_squared = correlation ** 2

# Calculate energy balance ratio
energy_ratio = y.sum() / x.sum()

# Plot
fig, ax = plt.subplots(figsize=(9, 8))

# Sample points for a clearer figure if necessary
plot_data = df.sample(
    n=min(20000, len(df)),
    random_state=42
)

ax.scatter(
    plot_data["Available_energy"],
    plot_data["Turbulent_energy"],
    alpha=0.2,
    s=8,
    label="Half-hourly observations"
)

# Reference line
lower = min(x.min(), y.min())
upper = max(x.max(), y.max())

ax.plot(
    [lower, upper],
    [lower, upper],
    linestyle="--",
    linewidth=2,
    label="1:1 reference"
)

# Regression line
line_x = np.linspace(lower, upper, 200)

ax.plot(
    line_x,
    slope * line_x + intercept,
    linewidth=2,
    label="Linear regression"
)

ax.set_xlabel(
    "Available energy: NETRAD − G (W m⁻²)"
)

ax.set_ylabel(
    "Turbulent energy: H + LE (W m⁻²)"
)

ax.set_title(
    "Energy balance closure: IT-TrF"
)

ax.grid(True, alpha=0.3)
ax.legend()

# Add statistics
statistics = (
    f"Slope = {slope:.3f}\n"
    f"R² = {r_squared:.3f}\n"
    f"Energy balance ratio = {energy_ratio:.3f}\n"
    f"Valid records = {len(df):,}"
)

ax.text(
    0.04, 0.96,
    statistics,
    transform=ax.transAxes,
    verticalalignment="top",
    bbox=dict(facecolor="white", alpha=0.8)
)

fig.tight_layout()

figure_path = output_folder / "energy_balance_IT-TrF.png"

fig.savefig(
    figure_path,
    dpi=300,
    bbox_inches="tight"
)

plt.close(fig)

# Save numerical results
summary = pd.DataFrame([{
    "SITE_ID": "IT-TrF",
    "Valid_records": len(df),
    "Regression_slope": slope,
    "Regression_intercept": intercept,
    "R_squared": r_squared,
    "Energy_balance_ratio": energy_ratio,
}])

summary_path = table_folder / "energy_balance_summary.csv"
summary.to_csv(summary_path, index=False)

print("\nENERGY BALANCE ANALYSIS COMPLETED")
print("=" * 55)
print(f"Site: IT-TrF")
print(f"Valid half-hourly records: {len(df):,}")
print(f"Regression slope: {slope:.3f}")
print(f"R-squared: {r_squared:.3f}")
print(f"Energy balance ratio: {energy_ratio:.3f}")
print(f"\nFigure saved: {figure_path}")
print(f"Summary saved: {summary_path}")
