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
from dotenv import load_dotenv
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser

load_dotenv()

llm = ChatGroq(model="llama-3.3-70b-versatile", max_tokens=1024)

embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

prompt = ChatPromptTemplate.from_template("""
You are a document assistant. Only answer questions based on the context provided.
If the answer is not in the context, say I don't know based on the given document.
Do not use outside knowledge. Do not generate code or answer unrelated questions.

Context:
{context}

Question:
{question}
""")

def ask_question(filepath, question):
    loader = TextLoader(filepath)
    docs = loader.load()

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50
    )
    chunks = splitter.split_documents(docs)

    vectorstore = Chroma.from_documents(chunks, embeddings)
    retriever = vectorstore.as_retriever()

    chain = (
        {"context": retriever, "question": RunnablePassthrough()}
        | prompt
        | llm
        | StrOutputParser()
    )

    return chain.invoke(question)