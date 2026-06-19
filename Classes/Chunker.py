from DataClasses.Page import Page
from DataClasses.Chunk import Chunk
from Classes.MyPDFReader import MyPDFReader

class Chunker:
    def __init__(self, pdf_reader: MyPDFReader, chunk_size: int, overlap: int):
        self.pdf_reader = pdf_reader
        self.chunk_size = chunk_size
        self.overlap = overlap
        self.chunks = self.chunk_pages()

    def chunk_pages(self) -> list[Chunk]:
        chunks = []
        for page in self.pdf_reader.get_pages():
            text = page.text
            page_number = page.page_number
            for i, chunk_text in enumerate(self.chunk_text(text)):
                chunks.append(Chunk(text=chunk_text, page_number=page_number, chunk_number=i + 1))
        return chunks
    
    def chunk_text(self, text: str) -> list[str]:
        if not text:
            return []
        chunks = []
        start = 0
        while start < len(text):
            target_end = min(start + self.chunk_size, len(text))
            end = target_end
            while (
                end < len(text)
                and text[end] not in ".!?"
                and end < target_end + 200
            ):
                end += 1
            if end < len(text):
                end += 1
            chunk = text[start:end].strip()
            if chunk:
                chunks.append(chunk)
            start += self.chunk_size - self.overlap
        return chunks
    
    def get_chunks(self) -> list[Chunk]:
        return self.chunks
