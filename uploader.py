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

headers_stream = {
    "Accept": "application/json",
    "Content-Type": "application/octet-stream",
    "Authorization": f"Bearer {credentials.api_key}"
}

def main():
    """
        For test purposes only.
    """
    metadata_file = "test/output.json"
    with open(metadata_file, "r") as f:
        metadata = json.load(f)    
        deposit(metadata, ["test/test1.txt", "test/test2.txt"])

def deposit(metadata, files):
    """
        Uploads and publishes a record to the repository.

        :param metadata: The record's DataCite metadata.
        :param files: The record's files.
    """
    record_id = upload(metadata, files)
    publish_record(record_id)


def create_draft_record(metadata):
    """
        Creates a draft record in the repository.
        Exits the program if the request fails.

        :param metadata: The record's metadata.
        :param files: The record's files.
        :returns: The record's id.
    """
    resp = requests.post(
        f"{api_url}/api/records", data=json.dumps(metadata), headers=headers, verify=False
    )
    
    if (resp.status_code != 201):
        print(f"Could not create record: {resp.status_code} {resp.text}")
        sys.exit(1)
    return resp.json().get("id")


def start_draft_files_upload(record_id, files):
    """
        Starts the draft file upload.
        This function does NOT upload any files, but initializes the upload process.
        Exits the program if the request fails.
        
        :param record_id: The record's id.
        :param files: The files to be uploaded.
    """
    payload = []
    for file in files:
        _, filename = os.path.split(file)
        payload.append({"key": filename})
    
    resp = requests.post(f"{api_url}/api/records/{record_id}/draft/files", data=json.dumps(payload), headers=headers, verify=False)
    if (resp.status_code != 201):
        print(f"Could not initiate file upload: {resp.status_code} {resp.text}")
        sys.exit(1)
    return


def upload_file(record_id, file_path):
    """
        Uploads a file to the record.
        Exits the program if the request fails.

        :param record_id: The record's id.
        :param file_path: The path of the file to upload.
    """
    _, file_name = os.path.split(file_path)
    print(file_name)

    # Upload file content
    with open(file_path, "r") as f:
            resp = requests.put(
                f"{api_url}/api/records/{record_id}/draft/files/{file_name}/content", data=f, headers=headers_stream, verify=False
            )
            if (resp.status_code != 200):
                print(f"Could not upload file content: {resp.status_code} {resp.text}")
                sys.exit(1)

    # Complete draft file upload
    resp = requests.post(f"{api_url}/api/records/{record_id}/draft/files/{file_name}/commit", headers=headers, verify=False)
    if (resp.status_code != 200):
        print(f"Could not commit file upload: {resp.status_code} {resp.text}")
        sys.exit(1)


def upload(metadata, files):
    """
        Uploads a draft record to the repository.
        Exits the program if the request fails.

        :param metadata: The record's metadata.
        :param files: The record's files.
        :returns: The draft record's id.
    """

    record_id = create_draft_record(metadata)
    start_draft_files_upload(record_id, files)

    for file in files:
        upload_file(record_id, file)
    return record_id

def publish_record(record_id):
    """
        Publishes a record.
        Exits the program if the request fails.

        :param record_id: The record's id.
    """
    resp = requests.post(
        f"{api_url}/api/records/{record_id}/draft/actions/publish", headers=headers, verify=False
    )
    if (resp.status_code != 202):
        print(f"Could not publish record: {resp.status_code} {resp.text}")
        sys.exit(1)

if __name__ == "__main__":
    main()