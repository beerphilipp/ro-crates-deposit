import sys
import requests
import credentials
import json

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
    
    if (len(sys.argv) != 3):
        print("Usage: python converter.py <input_file> <output_file>")
        sys.exit(1)
    
    input_file = sys.argv[1]
    output_file = sys.argv[2]


    upload("", [])

    # convert DataCite XML to DataCite JSON

def upload(metadata, files):
    """
        Uploads a record to the repository.
    """
    
    req = requests.post(
        f"{api_url}/api/records", data=json.dumps(metadata), headers=headers, verify=False
    )
    
    if (req.status_code != 201):
        print(f"Could not create record: {req.status_code} {req.text}")
        sys.exit(1)

    links = req.json()['links']
    
    files_link = links['files'] # used to upload files to the record

    for f_name in files:
        
        # Init file
        req = requests.post(
            files_link, data=json.dumps([{"key": f_name}]), headers=headers, verify=False
        )
        if (req.status_code != 201):
            print(f"Could not initiate file upload: {req.status_code} {req.text}")
            sys.exit(1)
        file_links = req.json()["entries"][0]["links"]

        # Upload file content
        with open(f_name, "r") as f:
            req = requests.put(
                file_links["content"], data=f, headers=headers_stream, verify=False
            )
            if (req.status_code != 200):
                print(f"Could not upload file content: {req.status_code} {req.text}")
                sys.exit(1)
        
        # Commit file upload
        requests.post(
            file_links["commit"], headers=headers, verify=False
        )
        if (req.status_code != 200):
            print(f"Could not commit file upload: {req.status_code} {req.text}")
            sys.exit(1)

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