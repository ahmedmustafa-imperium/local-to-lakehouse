# upload_to_fabric_final.py

import os
from pathlib import Path
from dotenv import load_dotenv
from azure.storage.filedatalake import DataLakeServiceClient
from azure.identity import ClientSecretCredential
from tqdm import tqdm 

# Load environment variables from .env file
load_dotenv()

# Read from .env
TENANT_ID     = os.getenv("TENANT_ID")
CLIENT_ID     = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")

WORKSPACE_NAME = os.getenv("WORKSPACE_NAME")
LAKEHOUSE_NAME = os.getenv("LAKEHOUSE_NAME")

LOCAL_FOLDER     = os.getenv("LOCAL_FOLDER")
TARGET_SUBFOLDER = os.getenv("TARGET_SUBFOLDER", "auto_uploaded")

# Validation
required = ["TENANT_ID", "CLIENT_ID", "CLIENT_SECRET", "WORKSPACE_NAME", "LAKEHOUSE_NAME", "LOCAL_FOLDER"]
missing = [var for var in required if not os.getenv(var)]
if missing:
    raise ValueError(f"Missing in .env: {', '.join(missing)}")

# Correct OneLake settings
ACCOUNT_URL = "https://onelake.dfs.fabric.microsoft.com"
FILESYSTEM  = WORKSPACE_NAME                                   # workspace name
LAKEHOUSE_PATH = f"{LAKEHOUSE_NAME}.Lakehouse/Files/{TARGET_SUBFOLDER}"

def upload_folder():
    # Authenticate with service principal
    credential = ClientSecretCredential(TENANT_ID, CLIENT_ID, CLIENT_SECRET)
    service_client = DataLakeServiceClient(account_url=ACCOUNT_URL, credential=credential)
    fs_client = service_client.get_file_system_client(FILESYSTEM)

    local_root = Path(LOCAL_FOLDER)
    if not local_root.exists():
        raise FileNotFoundError (f"Folder not found: {LOCAL_FOLDER}")

    # Collect all files first for progress bar
    files_to_upload = []
    for current_dir, _, files in os.walk(local_root):
        rel_dir = Path(current_dir).relative_to(local_root)
        for f in files:
            local_path = Path(current_dir) / f
            remote_path = f"{LAKEHOUSE_PATH}/{rel_dir}/{f}".replace("\\", "/").strip("/")
            files_to_upload.append((local_path, remote_path))

    print(f"Uploading {len(files_to_upload)} files to Lakehouse → Files/{TARGET_SUBFOLDER}/\n")

    # Upload with nice progress bar
    for local_path, remote_path in tqdm(files_to_upload, desc="Uploading", unit="file"):
        try:
            file_client = fs_client.get_file_client(remote_path)
            with open(local_path, "rb") as data:
                file_client.upload_data(data, overwrite=True)
        except Exception as e:
            print(f"\nFailed {local_path.name}: {e}")

    print(f"\nSUCCESS! All files uploaded.")
    print(f"Go to Fabric → Workspace '{WORKSPACE_NAME}' → Lakehouse '{LAKEHOUSE_NAME}' → Files → {TARGET_SUBFOLDER}")

if __name__ == "__main__":
    upload_folder()
