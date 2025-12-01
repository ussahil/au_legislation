import fitz
from pathlib import Path



def pdf_to_markdown(input_path:Path):
    doc = fitz.open(f"../data/raw_data/{input_path}.pdf")
    elements = []

    for page in doc:
        blocks = page.get_text("dict")['blocks']
        for b in blocks:
            if "lines"  not in b:
                continue
            for line in b['lines']:
                for span in line['spans']:
                    elements.append({
                        "text":span['text'],
                        "size":span['size'],
                        'font':span['font'],
                        "bold":"Bold" in span['font'],
                    })

# print(elements[0:20])

#  Lets get all the sizes and then based on the sizes I will add in 
# sizes = sorted({item['size']for item in elements},reverse=True)

#  First confirm the text that is in 8.0 , 9.0 if it is footers we shall ignore
# size_8 = []
# for item in elements:
#     if item['size'] == 9.0:
#         size_8.append(item['text'])

# Ignore size 8 defintely

    size_to_md = {
        20.0: "#",        # Act Title
        18.0: "##",       # Chapter
        16.0: "###",      # Part
        14.0: "####",     # Division
        13.0: "#####",    # Subdivision
        12.0: "######",   # Section heading
        11.5: "",         # Body text
        11.0: "",         # Body text
        10.0: "",       # Notes / Example / Supplementary
        9.0: "",        # Annotations
    }

    md_lines = []

    for item in elements:
        size = item['size']
        text = item['text'].strip()

        if not text:
            continue

        prefix = size_to_md.get(size,"")

        if prefix.startswith("#"):
            line = f"{prefix} {text}"

        else:
            line = text 

        md_lines.append(line)

    # output_path = "../../data/cleaned_data/C2025C00644VOL01.md"

    with  open(f"../data/cleaned_data/{input_path}.md","w",encoding="utf-8") as f:
        for line in md_lines:
            f.write(line + '\n')