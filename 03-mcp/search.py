import os
import zipfile
import requests
from minsearch import Index

ZIP_URL = "https://github.com/jlowin/fastmcp/archive/refs/heads/main.zip"
ZIP_NAME = "fastmcp-main.zip"

# Download zip if not present
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

def get_md_files_from_zip(zip_path):
    md_files = []
    with zipfile.ZipFile(zip_path, 'r') as z:
        for info in z.infolist():
            if info.filename.endswith(('.md', '.mdx')):
                # Remove the first part of the path
                parts = info.filename.split('/', 1)
                if len(parts) == 2:
                    filename = parts[1]
                else:
                    filename = info.filename
                with z.open(info) as f:
                    content = f.read().decode(errors='ignore')
                md_files.append({"filename": filename, "content": content})
    return md_files

def build_index(md_files):
    # Use correct minsearch API
    index = Index(text_fields=["content"], keyword_fields=["filename"])
    index.fit(md_files)
    return index

def search_index(index, query, k=5):
    return index.search(query, num_results=k)

def main():
    download_zip()
    md_files = get_md_files_from_zip(ZIP_NAME)
    index = build_index(md_files)
    print("Index built with", len(md_files), "documents.")
    # Example search
    results = search_index(index, "demo", k=5)
    for i, doc in enumerate(results, 1):
        print(f"Result {i}: {doc['filename']}")
        print(doc['content'][:200], "...\n")

if __name__ == "__main__":
    main()
