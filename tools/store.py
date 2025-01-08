import json
from typing import List, Dict
import pickle
from pathlib import Path
import psycopg2
from psycopg2 import Error
import google.generativeai as genai
from langchain.text_splitter import CharacterTextSplitter
import os

genai.configure(api_key=os.environ['NUXT_GEMINI'])

def load_chunks_from_json(filepath="chunks.json"):
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            chunks = json.load(f)
            print(f"Successfully loaded chunks from {filepath}")
            return chunks
    except Exception as e:
        print(f"Error loading chunks: {e}")
        return None

def convert_docs_to_dict(docs):
    return [
        {
            "page_content": doc.page_content,
            "metadata": doc.metadata
        }
        for doc in docs
    ]

def save_chunks_to_json(docs, filepath="chunks.json"):
    """Save chunks to JSON file, handling both document objects and dictionaries"""
    try:
        chunks_dict = docs if isinstance(docs[0], dict) else convert_docs_to_dict(docs)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(chunks_dict, f, indent=4, ensure_ascii=False)
        print(f"Successfully saved chunks to {filepath}")
    except Exception as e:
        print(f"Error saving chunks: {e}")
def connect_to_postgres_and_insert_data(data, connection_url):
    try:
        connection = psycopg2.connect(connection_url)
        cursor = connection.cursor()
        
        insert_query = """
        INSERT INTO mchunks (content, embedding, document_id)
        VALUES (%s, %s, %s)
        """
        count = 0
        total = len(data)
        for item in data:
            embedding = genai.embed_content(model="models/text-embedding-004", content=item['page_content'])
            cursor.execute(insert_query, (item['page_content'], embedding['embedding'], 2))
            print(str(count)+" of "+str(total))
        connection.commit()
        print("Data inserted successfully")
        cursor.close()
        connection.close()
    except Exception as e:
        print(f"Error connecting to PostgreSQL: {e}")

connection_url = os.environ['NUXT_DB_URI']


def reprocess_chunks_with_limit(chunks, max_chars=8000):
    processed_chunks = []
    text_splitter = CharacterTextSplitter(
        separator="\n",
        chunk_size=max_chars,
        chunk_overlap=200,
        length_function=len
    )
    
    for chunk in chunks:
        if len(chunk["page_content"]) > max_chars:
            split_docs = text_splitter.create_documents(
                [chunk["page_content"]], 
                metadatas=[chunk["metadata"]]
            )
            processed_chunks.extend(convert_docs_to_dict(split_docs))
        else:
            processed_chunks.append(chunk)
    
    return processed_chunks
loaded_chunks = load_chunks_from_json("m_output_chunks.json")
if loaded_chunks:
    limited_chunks = reprocess_chunks_with_limit(loaded_chunks)
    save_chunks_to_json(limited_chunks, "m_output_chunks_final.json")
connect_to_postgres_and_insert_data(limited_chunks, connection_url)