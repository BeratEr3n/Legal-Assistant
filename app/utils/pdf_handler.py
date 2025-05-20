import fitz
from typing import List
from langchain.schema import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter

#Verilen PDF dosyasından ilk max_pages (varsayılan 200) sayfasının metnini çıkarır.
def extract_text_from_pdf(pdf_path, max_pages: int = 200):
    """
        PDF'den ilk N sayfayı okuyarak metin çıkar.
    """
    try:
        pdf_doc = fitz.open(pdf_path)
    except Exception as e:
        print(f"PDF okuma hatası ({pdf_path}): {e}")
        return ""

    full_text = ""
    for i, page in enumerate(pdf_doc):
        if i >= max_pages:
            break
        full_text += page.get_text()
    
    return full_text

#Yüklenen PDF dosyasının metnini çıkarır, metni parçalara böler ve LangChain Document objeleri listesi olarak döner.
def process_uploaded_pdf(pdf_path) -> list[Document]:

    full_text = extract_text_from_pdf(pdf_path)

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len
    )
    chunks = text_splitter.split_text(full_text)

    documents = []
    for i, chunk in enumerate(chunks):
        doc = Document(
            page_content=chunk,
            metadata={
                "chunk": i,
                "document": pdf_path.split("/")[-1]
            }
        )
        documents.append(doc)

    return documents

# Karar metni gibi uzun metinleri parçalarına böler ve Document objeleri listesi döner.
def process_decisions_text(decisions_text: str, source_name: str = "yargitay_karar") -> list[Document]:
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len
    )
    chunks = text_splitter.split_text(decisions_text)
    
    documents = []
    for i, chunk in enumerate(chunks):
        doc = Document(
            page_content=chunk,
            metadata={
                "chunk": i,
                "source": source_name
            }
        )
        documents.append(doc)
    
    return documents