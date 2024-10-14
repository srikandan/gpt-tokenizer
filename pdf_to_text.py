import PyPDF2
import os

def pdf_to_text(pdf_path, output_path):
    # Open the PDF file in read-binary mode
    with open(pdf_path, 'rb') as file:
        # Create a PDF reader object
        pdf_reader = PyPDF2.PdfReader(file)
        
        # Get the number of pages in the PDF
        num_pages = len(pdf_reader.pages)
        
        # Open the output text file in write mode
        with open(output_path, 'w', encoding='utf-8') as out_file:
            # Iterate through all pages
            for page_num in range(num_pages):
                # Get the page object
                page = pdf_reader.pages[page_num]
                
                # Extract text from the page
                text = page.extract_text()
                
                # Write the extracted text to the output file
                out_file.write(text)
                
                # Add a newline character after each page (optional)
                out_file.write('\n')

    print(f"Conversion complete. Text saved to {output_path}")

# Example usage
pdf_path = r"G:\Books\Transformers and LLM\Build a Large Language Model (From Scratch)\Build_a_Large_Language_Model_(From_Scrat.pdf"  # Replace with your PDF file path
output_path = 'output.txt'  # Replace with your desired output text file path

pdf_to_text(pdf_path, output_path)