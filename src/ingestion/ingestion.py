from pathlib import Path
from langchain_core.documents import Document
from langchain_community.document_loaders import PyPDFLoader, TextLoader


class Ingestion:
    def __init__(self, directory: str):
        self.directory = directory

    
    def load_docs(self) -> list[Document]:
        documents = []

        for path in Path(self.directory).rglob('*'):
            if not path.is_file():
                continue

            if path.suffix.lower() == ".pdf":
                loader = PyPDFLoader(file_path=str(path))
                docs = loader.load()

            elif path.suffix.lower() in {".txt", ".md"}:
                loader = TextLoader(file_path=str(path), encoding='UTF-8')
                docs = loader.load()

            else:
                continue

            for doc in docs:
                doc.metadata['source'] = str(path)
                doc.metadata['file_name'] = path.name

            documents.extend(docs)
        return documents