
import csv
from pathlib import Path

processed_folder = Path("data/processed")
report_path = Path("output/tables/initial_data_check.txt")

required_variables = [
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

report = []

for csv_path in sorted(processed_folder.glob("*.csv")):
    report.append("\n" + "=" * 70)
    report.append(f"SITE FILE: {csv_path.name}")
    report.append("=" * 70)

    with csv_path.open(
        "r", encoding="utf-8-sig", newline=""
    ) as file:
        reader = csv.reader(file)

        headers = next(reader)

        report.append(f"Number of columns: {len(headers)}")

        # Identify date and time columns
        time_columns = [
            col for col in headers
            if any(term in col.upper()
                   for term in ["TIMESTAMP", "YEAR", "DOY", "DATE", "TIME"])
        ]

        report.append("\nTimestamp/date columns:")
        report.extend(time_columns if time_columns else ["None identified"])

        # Check required analysis variables
        report.append("\nRequired variable availability:")

        for variable in required_variables:
            status = "FOUND" if variable in headers else "MISSING"
            report.append(f"{variable}: {status}")

        # Show selected values from the first two records
        selected_columns = list(dict.fromkeys(
            time_columns + [
                variable for variable in required_variables
                if variable in headers
            ]
        ))

        report.append("\nFirst two data rows (selected columns):")

        for row_number, row in enumerate(reader):
            if row_number >= 2:
                break

            values = dict(zip(headers, row))

            for column in selected_columns:
                report.append(
                    f"  {column}: {values.get(column, 'Not available')}"
                )

            report.append("")

report_path.parent.mkdir(parents=True, exist_ok=True)
report_path.write_text("\n".join(report), encoding="utf-8")

print("Inspection completed.")
print(f"Report saved to: {report_path}")
print(f"Files inspected: {len(list(processed_folder.glob('*.csv')))}")
