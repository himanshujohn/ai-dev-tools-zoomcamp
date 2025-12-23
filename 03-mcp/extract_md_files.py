def search_index(index, query, num_results=5):
    """
    Search the index for the most relevant documents.
    Returns a list of dicts with 'filename' and 'content'.
    """
    results = index.search(query, num_results=num_results)
    return results
import zipfile
import os
from minsearch import Index

ZIP_NAME = "fastmcp-main.zip"

def get_md_files_from_zip(zip_path):
    md_files = []
    with zipfile.ZipFile(zip_path, 'r') as z:
        for info in z.infolist():
            if info.filename.endswith(('.md', '.mdx')):
                # Remove the first part of the path (before the first slash)
                filename = info.filename
                if '/' in filename:
                    filename = filename.split('/', 1)[1]
                with z.open(info) as f:
                    content = f.read().decode(errors='ignore')
                md_files.append({"filename": filename, "content": content})
    return md_files

def build_index(md_files):
    # Use Index with text_fields=["content"], keyword_fields=["filename"]
    index = Index(text_fields=["content"], keyword_fields=["filename"])
    index.fit(md_files)
    return index

if __name__ == "__main__":
    if not os.path.exists(ZIP_NAME):
        print(f"{ZIP_NAME} not found. Please download it first.")
    else:
        md_files = get_md_files_from_zip(ZIP_NAME)
        print(f"Found {len(md_files)} markdown files.")
        index = build_index(md_files)
        print(f"Indexed {len(md_files)} documents with minsearch.")

        # Example usage: search for a query if provided as argument
        import sys
        if len(sys.argv) > 1:
            query = " ".join(sys.argv[1:])
            results = search_index(index, query)
            print(f"Top {len(results)} results for query: '{query}'\n")
            for i, doc in enumerate(results, 1):
                print(f"Result {i}: {doc['filename']}")
                print(doc['content'][:300].replace('\n', ' '))
                print("-"*40)
