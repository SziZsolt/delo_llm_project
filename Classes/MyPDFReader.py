from pypdf import PdfReader
import re
from Page import Page

class MyPDFReader:
    def __init__(self, file_path: str):
        self.file_path = file_path
        self.reader = PdfReader(self.file_path)
        self.pages = self.load_pages(self.reader)
    
    def process_page(self, page_text: str) -> str:
        page_text = re.sub(r'\s+', ' ', page_text)
        page_text = page_text.replace('\n', ' ')
        page_text = page_text.strip()
        return page_text
    
    def load_pages(self) -> list[Page]:
        pages = []
        for i, page in enumerate(self.reader.pages):
            text = page.extract_text() or ''
            text = self.process_page(text)
            pages.append(Page(text=text, page_number=i+1))
        return pages
    
    def get_pages(self) -> list[Page]:
        return self.pages