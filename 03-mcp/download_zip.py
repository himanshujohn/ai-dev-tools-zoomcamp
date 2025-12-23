import os
import requests

ZIP_URL = "https://github.com/jlowin/fastmcp/archive/refs/heads/main.zip"
ZIP_NAME = "fastmcp-main.zip"

def download_zip():
    if not os.path.exists(ZIP_NAME):
        print(f"Downloading {ZIP_URL}...")
        r = requests.get(ZIP_URL)
        r.raise_for_status()
        with open(ZIP_NAME, "wb") as f:
            f.write(r.content)
        print("Download complete.")
    else:
        print(f"{ZIP_NAME} already exists.")

if __name__ == "__main__":
    download_zip()
