from utils.clean import pdf_to_markdown


law_files = ["C2025C00644VOL01","C2025C00644VOL02","C2025C00644VOL03","C2025C00644VOL04"]

if __name__ == "__main__":
    
    for law_file in law_files:
        pdf_to_markdown(law_file)