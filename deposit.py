"""
    This script deposits a RO-Crate directory to the TU Data repository.
"""
import sys
import os
import json
import glob

import converter
import uploader

def main():
    if (len(sys.argv) != 2):
        print("Usage: python deposit.py <ro-crate-directory>")
        sys.exit(1)

    ro_crates_dir = sys.argv[1]

    all_files = []
    for file in glob.glob(f"{ro_crates_dir}/**", recursive=True):
        if (file.endswith("ro-crate-metadata.json")):
            continue
        if (os.path.isfile(file)):
            all_files.append(file)

    ro_crates_metadata_file = os.path.join(ro_crates_dir, "ro-crate-metadata.json")

    if (not os.path.isfile(ro_crates_metadata_file)):
        print(f"'{ro_crates_dir}' is not a RO-Crate directory: 'ro-crate-matadata.json' not found.")
        sys.exit()
    
    with open(ro_crates_metadata_file, "r") as f:
        ro_crate_metadata = json.load(f)

    # Convert Metadata
    data_cite_metadata = converter.convert(ro_crate_metadata)

    # Upload files
    uploader.deposit(data_cite_metadata, all_files)


if __name__ == "__main__":
    main()