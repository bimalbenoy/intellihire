import io
import os   #in case it is running locally to get files from disk
from pdfminer.high_level import extract_text as extract_pdf
import docx

def extract(file_path: str) -> str:
    if file_path.endswith('pdf'):
        return extract_pdf(file_path)
    elif file_path.endswith('docx'):
        doc = docx.Document(file_path)
        return "/n".join(p.text for p in doc.paragraphs)
    else:
        raise ValueError("Unsupported file type.")
    
if __name__ == "__main__":  #runs only when executed directly(in main function)
    input_dir = "test_resumes"  #enter the directory from which to access
    for filename in os.listdir(input_dir):  #this is to access local files make changes as necessary
        if filename.endswith(('.pdf','.docx')):
            file_path = os.path.join(input_dir,filename) #for local files make changes as necassary when using flask
            text = extract(file_path)
print(text)
