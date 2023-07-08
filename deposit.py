"""
    This script deposits a RO-Crate directory to an InvenioRDM repository.
    
    :author: Philipp Beer
    :author: Milan Szente
"""
import sys
import os
import json
import glob
import argparse

import mapping.converter as converter
import upload.uploader as uploader

def main():
    """
        The main function of the script.
        It takes a RO-Crate directory as input and uploads it to an InvenioRDM repository.
    """

    parser = argparse.ArgumentParser(
                    description='Takes a RO-Crate directory as input and uploads it to an InvenioRDM repository')
    
    parser.add_argument('ro_crate_directory', help='RO-Crate directory to upload.', type=str, action='store')
    parser.add_argument('-d', '--datacite', help="Optional DataCite metadata file. Skips the conversion process.", type=str, action='store', nargs=1)
    parser.add_argument('-p', '--publish', help="Publish the record after uploading.", action='store_true')
    args = parser.parse_args()

    ro_crates_dir = args.ro_crate_directory
    datacite_list = args.datacite
    publish = args.publish

    datacite_file = None
    skip_conversion = False
    if (datacite_list):
        datacite_file = datacite_list[0]
        skip_conversion = True
        

    # Get all files in RO-Crate directory and check if it is a RO-Crate directory
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
    
    if (not skip_conversion):
        with open(ro_crates_metadata_file, "r") as f:
            ro_crate_metadata = json.load(f)

        metadata_only = False
        if len(all_files) == 0:
            metadata_only = True

        # Convert Metadata
        data_cite_metadata = converter.convert(ro_crate_metadata, metadata_only=metadata_only)
        # store datacite metadata
        with open("datacite-out.json.json", "w") as f:
            json.dump(data_cite_metadata, f, indent=4)
    else:
        with open(datacite_file, "r") as f:
            data_cite_metadata = json.load(f)

    # Upload files
    uploader.deposit(data_cite_metadata, all_files, publish=publish)


if __name__ == "__main__":
    main()