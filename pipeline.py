# import os
# from groq import Groq
# from dotenv import load_dotenv
# from utils import read_file, chunk_text

# load_dotenv()

# client = Groq()

# def find_relevant_chunks(chunks, question):
#     relevant = []
#     question_words = question.lower().split()

#     for chunk in chunks:
#         chunk_lower = chunk.lower()
#         for word in question_words:
#             if word in chunk_lower:
#                 relevant.append(chunk)
#                 break

#     if not relevant:
#         relevant = chunks[:2]

#     return relevant

# def ask_question(filepath, question):
#     text = read_file(filepath)
#     chunks = chunk_text(text)
#     relevant_chunks = find_relevant_chunks(chunks, question)
#     context = "\n\n".join(relevant_chunks)

#     response = client.chat.completions.create(
#         model="llama-3.3-70b-versatile",
#         max_tokens=1024,
#         messages=[
#             {
#                 "role": "system",
#                 "content": "You are a document assistant. Only answer questions based on the context provided. If the answer is not in the context, say I don't know based on the given document. Do not use outside knowledge. Do not generate code or answer unrelated questions."
#             },
#             {
#                 "role": "user",
#                 "content": f"Context:\n{context}\n\nQuestion:\n{question}"
#             }
#         ]
#     )

#     return response.choices[0].message.content


import os
import hashlib
import pandas as pd
from dotenv import load_dotenv
from langchain_community.document_loaders import TextLoader
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.document_loaders import Docx2txtLoader
from langchain_community.document_loaders import DataFrameLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
# from langchain_community.vectorstores import Chroma
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

load_dotenv()

llm = ChatGroq(model="llama-3.3-70b-versatile", max_tokens=1024)

embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

prompt = ChatPromptTemplate.from_template("""
You are a document assistant. Answer questions based on the context provided.
If the question is a follow up to the previous conversation, use the conversation history to understand what is being asked.
If the answer is not in the context or history, say I don't know based on the given document.
Do not use outside knowledge unrelated to the document. Do not generate code.

Previous conversation:
{history}

Context:
{context}

Question:
{question}
""")

conversation_store = {}

LOADERS = {
    ".pdf":  PyPDFLoader,
    ".txt":  TextLoader,
    ".docx": Docx2txtLoader,
}

VECTOR_DB_ROOT = "./chroma_db"


def load_document(filepath):
    ext = os.path.splitext(filepath)[1].lower()

    if ext in [".xlsx", ".xls"]:
        df = pd.read_excel(filepath)
        df = df.astype(str)
        df["combined"] = df.apply(lambda row: " | ".join(row.values), axis=1)
        loader = DataFrameLoader(df, page_content_column="combined")
        return loader.load()

    if ext not in LOADERS:
        raise ValueError(f"Unsupported file type: {ext}")

    loader = LOADERS[ext](filepath)
    return loader.load()


def get_collection_name(filepath):
    """
    Creates a unique, safe folder name for this file.
    Based on filename + last modified time, so if the file changes,
    a new embedding gets created automatically instead of using a stale one.
    """
    abs_path = os.path.abspath(filepath)
    last_modified = os.path.getmtime(abs_path)
    fingerprint = f"{abs_path}-{last_modified}"
    return hashlib.md5(fingerprint.encode()).hexdigest()


def get_vectorstore(filepath):
    collection_name = get_collection_name(filepath)
    persist_path = os.path.join(VECTOR_DB_ROOT, collection_name)

    if os.path.exists(persist_path):
        # Already embedded before — just load it, no re-embedding
        print(f"[CACHE HIT] Loading existing vector store for {filepath}")
        vectorstore = Chroma(
            persist_directory=persist_path,
            embedding_function=embeddings
        )
    else:
        # First time seeing this file — embed it and save to disk
        print(f"[CACHE MISS] Embedding {filepath} for the first time")
        docs = load_document(filepath)

        splitter = RecursiveCharacterTextSplitter(
            chunk_size=500,
            chunk_overlap=50
        )
        chunks = splitter.split_documents(docs)

        vectorstore = Chroma.from_documents(
            chunks,
            embeddings,
            persist_directory=persist_path
        )

    return vectorstore


def format_history(session_id):
    history = conversation_store.get(session_id, [])
    if not history:
        return "No previous conversation."

    formatted = ""
    for turn in history:
        formatted += f"User: {turn['question']}\n"
        formatted += f"Assistant: {turn['answer']}\n\n"
    return formatted


def ask_question(filepath, question, session_id):
    vectorstore = get_vectorstore(filepath)
    retriever = vectorstore.as_retriever()

    history = format_history(session_id)
    context_docs = retriever.invoke(question)
    context = "\n\n".join([doc.page_content for doc in context_docs])

    chain = prompt | llm | StrOutputParser()

    answer = chain.invoke({
        "history": history,
        "context": context,
        "question": question
    })

    if session_id not in conversation_store:
        conversation_store[session_id] = []

    conversation_store[session_id].append({
        "question": question,
        "answer": answer
    })

    return answer