import zipfile
from bs4 import BeautifulSoup

# Path to your EPUB
epub_path = "../../data/raw_data/C2025C00644.epub"

epub_contents = {}

with zipfile.ZipFile(epub_path, 'r') as epub:
    # List all files inside
    all_files = epub.namelist()
    
    # Filter HTML files (your chapters)
    html_files = [f for f in all_files if f.endswith(".html")]

    for html_file in html_files:
        content = epub.read(html_file)
        soup = BeautifulSoup(content, "html.parser")

        elements = []

        # Extract headings
        for level in range(1, 7):
            for h in soup.find_all(f"h{level}"):
                elements.append({
                    "type": "heading",
                    "level": level,
                    "text": h.get_text(strip=True)
                })

        # Extract paragraphs
        for p in soup.find_all("p"):
            text = p.get_text(strip=True)
            if text:
                elements.append({
                    "type": "paragraph",
                    "text": text
                })

        epub_contents[html_file] = elements

# Now epub_contents contains all the HTML files with headings & paragraphs
# Example: to access document_1 content
# print(epub_contents['OEBPS/document_1/document_1.html'])
first_key = list(epub_contents.keys())[0]
first_value = epub_contents[first_key]

print("First key:", first_key)
print("First value:", first_value[:100])