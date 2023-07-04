import sys
import requests
import credentials
import json
import os
import time
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

api_url = "https://test.researchdata.tuwien.ac.at/"

publish = False

headers = {
    "Accept": "application/json",
    "Content-Type": "application/json",
    "Authorization": f"Bearer {credentials.api_key}"    
}

h = {
    "Accept": "application/json",
    "Authorization": f"Bearer {credentials.api_key}"
}

headers_stream = {
    "Accept": "application/json",
    "Content-Type": "application/octet-stream",
    "Authorization": f"Bearer {credentials.api_key}"
}

def main():
    
    if (len(sys.argv) != 3):
        print("Usage: python converter.py <input_file> <output_file>")
        sys.exit(1)
    
    input_file = sys.argv[1]
    output_file = sys.argv[2]

    metadata_file = "test/output.json"
    with open(metadata_file, "r") as f:
        metadata = json.load(f)    
        upload(metadata, ["test/test1.txt", "test/test2.txt"])

    # convert DataCite XML to DataCite JSON


def create_draft_record(metadata, files):
    """
        Creates a draft record in the repository.
        Exits the program if the request fails.

        :param metadata: The record's metadata.
        :param files: The record's files.
        :returns: The link to upload the record's files.
    """
    resp = requests.post(
        f"{api_url}/api/records", data=json.dumps(metadata), headers=headers, verify=False
    )
    print(resp)
    
    if (resp.status_code != 201):
        print(f"Could not create record: {resp.status_code} {resp.text}")
        sys.exit(1)

    links = resp.json()['links']
    files_link = links['files'] # used to upload files to the record
    return files_link


def upload_file(files_link, file_path):
    """
        Uploads a file to the record.
        Exits the program if the request fails.

        :param files_link: The link to upload the record's files.
        :param file_path: The path of the file to upload.
    """
    _, file_name = os.path.split(file_path)
    print(file_name)

    # Start draft file upload
    resp = requests.post(files_link, data=json.dumps([{"key": file_name}]), headers=headers, verify=False)
    if (resp.status_code != 201):
        print(f"Could not initiate file upload: {resp.status_code} {resp.text}")
        sys.exit(1)
    file_links = resp.json()["entries"][0]["links"]
    print(resp.json())

    # Upload file content
    with open(file_path, "r") as f:
            resp = requests.put(
                file_links["content"], data=f, headers=headers_stream, verify=False
            )
            if (resp.status_code != 200):
                print(f"Could not upload file content: {resp.status_code} {resp.text}")
                sys.exit(1)

    # Complete draft file upload
    resp = requests.post(file_links['commit'], headers=h, verify=False)
    if (resp.status_code != 200):
        print(f"Could not commit file upload: {resp.status_code} {resp.text}")
        sys.exit(1)


def upload(metadata, files):
    """
        Uploads a record to the repository.
    """

    files_link= create_draft_record(metadata, files)

    for file in files:
        upload_file(files_link, file)
        time.sleep(2)
    return

    if publish:
        # Publish record
        req = requests.post(
            links["publish"], headers=headers, verify=False
        )

        if (req.status_code != 202):
            print(f"Could not publish record: {req.status_code} {req.text}")
            sys.exit(1)

if __name__ == "__main__":
    main()