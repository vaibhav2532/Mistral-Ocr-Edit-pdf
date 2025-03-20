import os
from mistralai import Mistral

def extract_text_and_images(api_key, pdf_url, output_folder):
    client = Mistral(api_key=api_key)

    document = {"type": "document_url", "document_url": pdf_url}

    # Send request to Mistral OCR
    ocr_response = client.ocr.process(model="mistral-ocr-latest", document=document, include_image_base64=True)

    # Create output folder if it doesn't exist
    os.makedirs(output_folder, exist_ok=True)

    text_output_path = os.path.join(output_folder, "extracted_text.txt")
    with open(text_output_path, "w", encoding="utf-8") as text_file:
        for page_number, page in enumerate(ocr_response.pages, start=1):
            text = page.markdown if hasattr(page, "markdown") else ""
            text_file.write(f"--- Page {page_number} ---\n")
            text_file.write(text + "\n\n")

    print(f"Text extracted and saved to: {text_output_path}")

# Example usage
api_key = "CXsHK3JaT4LaVA3vjjbHLeEaFxf1CBwU"  # Replace with your actual API key
pdf_url = "https://drive.google.com/drive/u/1/home"  # Replace with your actual PDF URL
output_dir = "output"
extract_text_and_images(api_key, pdf_url, output_dir)



#https://pdf.ac/1dztsy