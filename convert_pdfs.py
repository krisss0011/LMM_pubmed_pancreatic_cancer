import os
from PyPDF2 import PdfReader

def convert_pdfs_to_txt(pdf_folder, output_folder):
    # Ensure the output folder exists
    os.makedirs(output_folder, exist_ok=True)

    # Iterate over all PDF files in the folder
    for filename in os.listdir(pdf_folder):
        if filename.endswith(".pdf"):
            pdf_path = os.path.join(pdf_folder, filename)
            try:
                print(f"Processing {filename}...")
                
                # Read the PDF
                reader = PdfReader(pdf_path)
                text = ""
                for page in reader.pages:
                    text += page.extract_text()

                # Save the extracted text to a .txt file
                txt_filename = os.path.splitext(filename)[0] + ".txt"
                txt_path = os.path.join(output_folder, txt_filename)
                with open(txt_path, "w", encoding="utf-8") as txt_file:
                    txt_file.write(text)
                
                print(f"Saved {txt_filename} to {output_folder}")
            except Exception as e:
                print(f"Error processing {filename}: {e}")

# Example usage
if __name__ == "__main__":
    pdf_folder = "C:/Users/krist/Desktop/Faks/Magisterij 2. letnik/Magistrski raziskovalni seminar/pubmed/biljana_pdf"
    output_folder = "C:/Users/krist/Desktop/Faks/Magisterij 2. letnik/Magistrski raziskovalni seminar/pubmed/xxx"
    convert_pdfs_to_txt(pdf_folder, output_folder)
