# Document Q&A Pipeline

A RAG (Retrieval Augmented Generation) pipeline built from scratch using Python, LangChain, and Flask.

## What it does
Upload any text document and ask questions about it. The pipeline finds relevant sections and uses an LLM to generate accurate answers.

## Tech Stack
- Python
- LangChain
- HuggingFace Embeddings
- ChromaDB (Vector Store)
- Groq LLM API (LLaMA 3.3 70b)
- Flask REST API

## How it works
1. Document is loaded and split into chunks
2. Chunks are converted to embeddings using HuggingFace
3. Embeddings stored in ChromaDB vector store
4. Question is matched to relevant chunks using semantic search
5. Relevant chunks + question sent to LLM
6. Answer returned via Flask API

## API Usage
POST /ask
{
  "question": "What is machine learning?",
  "filepath": "sample.txt"
}

## Setup
pip install -r requirements.txt
Add GROQ_API_KEY to .env file
python app.py
