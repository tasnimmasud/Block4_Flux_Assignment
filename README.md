# FLUXNET Block 4 Assignment
## Environmental Monitoring and Data Analysis

### Project overview

This project analyses half-hourly FLUXNET eddy-covariance data from five ecosystem monitoring sites:

- **CZ-Stn** – Stitna, Czech Republic
- **IT-TrF** – Torgnon-LD, Italy
- **NZ-ADw** – Ashley Dene wet, New Zealand
- **US-UiC** – University of Illinois Maize-Soy, USA
- **CN-YaS** – Yanchi natural shrubland, China

The analysis examines meteorological conditions, net ecosystem exchange (NEE), gross primary production (GPP), ecosystem respiration (RECO), seasonal patterns and energy balance.

### Data sources

Data were obtained from FLUXNET using the FLUXNET Shuttle snapshot:

`fluxnet_shuttle_snapshot_20261119T130245.csv`

Product version: **v1.3_r1**.

The five original ZIP archives are stored locally in `data/raw/`. The data directory is excluded from Git because of the large file sizes and data licensing conditions.

### Repository structure

```text
Block 04/
├── data/                  # Local data directory (not uploaded to GitHub)
│   ├── raw/
│   ├── snapshots/
│   └── processed/
├── scripts/
│   ├── extract_half_hourly.py
│   ├── prepare_data.py
│   ├── daily_timeseries.py
│   ├── seasonal_diurnal_cycles.py
│   ├── summary_statistics.py
│   ├── nee_coverage_heatmap.py
│   └── energy_balance.py
├── output/
│   ├── figures/
│   └── tables/
├── scripts/fluxnet_assignment.ipynb
├── fluxnet_assignment.html
├── .gitignore
└── README.md
```

### Software requirements

- Python 3.13
- pandas
- numpy
- matplotlib
- seaborn
- Jupyter Notebook
- fluxnet-shuttle
- Basemap

### Environment setup

Create and activate a virtual environment:

```powershell
py -3.13 -m venv .venv313
.\.venv313\Scripts\Activate.ps1
```

Install the required packages:

```powershell
python -m pip install pandas numpy matplotlib seaborn jupyter fluxnet-shuttle basemap
```

### Data preparation

Place the five original FLUXNET ZIP archives in `data/raw/`.

Extract the half-hourly files:

```powershell
python scripts/extract_half_hourly.py
```

Prepare the data:

```powershell
python scripts/prepare_data.py
```

The preparation process converts the FLUXNET missing-value code `-9999` to missing values and parses the timestamps as dates.

### Analysis

The analysis scripts generate the figures and tables used in the report:

- Data quality and annual NEE coverage
- Summary statistics
- Daily carbon-flux time series
- Seasonal diurnal cycles
- Energy balance analysis

The complete analysis and interpretation are presented in `fluxnet_assignment.html` and `scripts/fluxnet_assignment.ipynb`.

### Methodological choices

- NEE: `NEE_CUT_REF` (constant u* threshold method).
- GPP and RECO: nighttime partitioning (`GPP_NT_CUT_REF` and `RECO_NT_CUT_REF`).
- Air temperature: consolidated variable `TA_F`.
- Missing values: `-9999` treated as missing.

### References

Pastorello, G., Trotta, C., Canfora, E., et al. (2020). The FLUXNET2015 dataset and the ONEFlux processing pipeline for eddy covariance data. *Scientific Data*, 7, 225. https://doi.org/10.1038/s41597-020-0534-3

Site-specific dataset citations and the FLUXNET data acknowledgement are provided in the assignment report.

### License and acknowledgement

FLUXNET data are subject to their respective data-use and attribution terms. Please consult the original dataset documentation and provide the required site-specific citations and acknowledgements when using these data.