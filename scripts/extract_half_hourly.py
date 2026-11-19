
import zipfile
import shutil
from pathlib import Path

raw_folder = Path("data/raw")
processed_folder = Path("data/processed")

processed_folder.mkdir(parents=True, exist_ok=True)

archives = sorted(raw_folder.glob("*.zip"))

if len(archives) != 5:
    raise RuntimeError(
        f"Expected 5 ZIP archives, but found {len(archives)}."
    )

for zip_path in archives:
    print(f"\nProcessing: {zip_path.name}")

    with zipfile.ZipFile(zip_path, "r") as archive:

        matches = [
            name for name in archive.namelist()
            if "FLUXMET_HH_" in Path(name).name
            and name.lower().endswith(".csv")
            and "ERA5" not in Path(name).name
        ]

        if len(matches) != 1:
            raise RuntimeError(
                f"Expected one measured HH CSV in {zip_path.name}; "
                f"found {len(matches)}."
            )

        member = matches[0]
        output_path = processed_folder / Path(member).name

        if output_path.exists():
            print(f"Already exists, not overwritten: {output_path.name}")
            continue

        temporary_path = output_path.with_suffix(
            output_path.suffix + ".part"
        )

        try:
            with archive.open(member) as source:
                with temporary_path.open("wb") as destination:
                    shutil.copyfileobj(source, destination)

            temporary_path.replace(output_path)

        except Exception:
            temporary_path.unlink(missing_ok=True)
            raise

        print(f"Extracted: {output_path.name}")
        print(f"Size: {output_path.stat().st_size:,} bytes")

print("\nEXTRACTION CHECK")
print(
    "CSV files in processed folder:",
    len(list(processed_folder.glob("*.csv")))
)
print("Extraction step finished.")
