"""
Extract text from COVID-19 eBook PDF
"""
try:
    import PyPDF2
    print("PyPDF2 is installed")
except ImportError:
    print("Installing PyPDF2...")
    import subprocess
    subprocess.check_call(['pip', 'install', 'PyPDF2'])
    import PyPDF2

pdf_path = r"C:\Users\Manish\Downloads\covid19_ebook.pdf"
output_path = r"C:\Users\Manish\Desktop\COVID-19 vaccine tracker\extracted_ebook_text.txt"

print(f"Extracting text from: {pdf_path}")

with open(pdf_path, 'rb') as pdf_file:
    pdf_reader = PyPDF2.PdfReader(pdf_file)
    num_pages = len(pdf_reader.pages)
    
    print(f"Total pages: {num_pages}")
    
    extracted_text = []
    
    for page_num in range(num_pages):
        page = pdf_reader.pages[page_num]
        text = page.extract_text()
        extracted_text.append(f"\n--- PAGE {page_num + 1} ---\n")
        extracted_text.append(text)
    
    full_text = "".join(extracted_text)
    
    with open(output_path, 'w', encoding='utf-8') as output_file:
        output_file.write(full_text)
    
    print(f"\n✅ Extraction complete!")
    print(f"Text saved to: {output_path}")
    print(f"Total characters extracted: {len(full_text)}")
