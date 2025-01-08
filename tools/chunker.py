from langchain_experimental.text_splitter import SemanticChunker
from langchain_google_genai import GoogleGenerativeAIEmbeddings
import os
embeddings = GoogleGenerativeAIEmbeddings(model="models/text-embedding-004", google_api_key=os.environ['NUXT_GEMINI'])
from pathlib import Path
import json

text_splitter = SemanticChunker(embeddings)

def read_markdown_file(file_path):
    path = Path(file_path)
    if not path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")
    return path.read_text(encoding='utf-8')

def convert_docs_to_dict(docs):
    return [
        {
            "page_content": doc.page_content,
            "metadata": doc.metadata
        }
        for doc in docs
    ]

def save_chunks_to_json(docs, filepath="chunks.json"):
    try:
        chunks_dict = convert_docs_to_dict(docs)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(chunks_dict, f, indent=4, ensure_ascii=False)
        print(f"Successfully saved chunks to {filepath}")
    except Exception as e:
        print(f"Error saving chunks: {e}")

markdown_text = read_markdown_file("doc1_edited.md")
docs = text_splitter.create_documents([markdown_text])

save_chunks_to_json(docs, "m_output_chunks.json")