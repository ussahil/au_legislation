import fitz
from pathlib import Path


def pdf_to_markdown(input_path: Path):

    doc = fitz.open(f"../data/raw_data/{input_path}.pdf")
    elements = []

    for page in doc:
        blocks = page.get_text("dict", flags=fitz.TEXT_PRESERVE_LB)['blocks']

        for b in blocks:
            if "lines" not in b:
                continue

            for line in b["lines"]:
                for span in line["spans"]:
                    x0, y0, x1, y1 = span["bbox"]

                    elements.append({
                        "text": span["text"].strip(),
                        "size": span["size"],
                        "font": span["font"],
                        "bold": "Bold" in span["font"],
                        "x0": x0,
                        "y0": y0,
                        "y1": y1,
                    })

    # Remove empty strings
    elements = [e for e in elements if e["text"]]

    # Ignore clear footer text (font size 8 or 9, tiny indent)
    def is_footer(e):
        return e["size"] <= 9.5 and e["x0"] < 120

    elements = [e for e in elements if not is_footer(e)]

    # --- HEADING CLASSIFICATION LOGIC ---
    def classify(e):
        size = e["size"]
        bold = e["bold"]
        x0 = e["x0"]

        # Size-based primary hierarchy
        if size >= 20:
            return "#"
        if size >= 18:
            return "##"
        if size >= 16:
            return "###"
        if size >= 14:
            return "####"
        if size >= 13:
            return "#####"

        # Section heading (most PDFs)
        if size == 12 and bold:
            return "######"

        # Paragraph indentation logic
        if x0 < 60:
            return ""  # main paragraph
        if x0 < 80:
            return ""  # subparagraph
        if x0 < 120:
            return ""  # deeper

        return ""  # default body

    # --- BUILD MARKDOWN ---
    md_lines = []

    prev_y1 = None  # for line-gap detection

    for e in elements:
        prefix = classify(e)
        text = e["text"]

        # Extra spacing if large gap before line = heading
        if prev_y1 is not None:
            line_gap = e["y0"] - prev_y1
            if line_gap > 8 and prefix.startswith("#"):
                md_lines.append("")  # blank line before heading

        if prefix:
            md_lines.append(f"{prefix} {text}")
        else:
            md_lines.append(text)

        prev_y1 = e["y1"]

    # Output
    output_file = f"../data/cleaned_data/{input_path}.md"
    with open(output_file, "w", encoding="utf-8") as f:
        f.write("\n".join(md_lines))

    print(f"Markdown written to: {output_file}")
