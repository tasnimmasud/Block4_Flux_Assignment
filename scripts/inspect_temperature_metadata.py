
import zipfile
from pathlib import Path

# Locate the original US-UiC ZIP archive
raw_folder = Path("data/raw")
zip_files = list(raw_folder.glob("*US-UiC*.zip"))

if len(zip_files) != 1:
    raise RuntimeError(
        f"Expected one US-UiC ZIP file, found {len(zip_files)}"
    )

zip_path = zip_files[0]

print("US-UiC archive:", zip_path.name)

# Open the ZIP without extracting or modifying it
with zipfile.ZipFile(zip_path, "r") as archive:

    # Find the BIFVARINFO metadata file
    metadata_files = [
        name for name in archive.namelist()
        if "BIFVARINFO" in name.upper()
    ]

    if not metadata_files:
        raise RuntimeError("No BIFVARINFO file found in the archive.")

    print("\nBIFVARINFO files found:")
    for name in metadata_files:
        print(name)

    # Search metadata for the three temperature variables
    terms = ["TA_F_MDS", "TA_F", "TA_ERA"]

    for metadata_name in metadata_files:
        print("\n" + "=" * 75)
        print("METADATA FILE:", metadata_name)
        print("=" * 75)

        content = archive.read(metadata_name)
        text_content = content.decode(
            "utf-8-sig",
            errors="replace"
        )

        matching_lines = []

        for line in text_content.splitlines():
            if any(term in line for term in terms):
                matching_lines.append(line)

        if matching_lines:
            for line in matching_lines:
                print(line)
        else:
            print("No matching variable descriptions found.")

print("\nMETADATA INSPECTION COMPLETED")
