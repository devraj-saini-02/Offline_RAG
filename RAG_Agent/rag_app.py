# rag_app.py
import os
from langchain_chroma import Chroma
from langchain_ollama import OllamaEmbeddings, ChatOllama
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.prompts import ChatPromptTemplate

CHROMA_DIR = "chroma_db"

EMBED_MODEL = "nomic-embed-text"
LLM_MODEL   = "llama3.2"

embeddings = OllamaEmbeddings(model=EMBED_MODEL)

vector_store = Chroma(
    collection_name="project_rag_collection",
    embedding_function=embeddings,
    persist_directory=CHROMA_DIR
)

llm = ChatOllama(model=LLM_MODEL, temperature=0)


def ingest_pdf(project_name, file_path, file_name):
    try:
        loader = PyPDFLoader(file_path)
        raw_docs = loader.load()

        for doc in raw_docs:
            doc.metadata["project"] = project_name
            doc.metadata["source"] = file_name

        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000, chunk_overlap=200
        )
        chunks = text_splitter.split_documents(raw_docs)

        vector_store.add_documents(chunks)
        print(f"[RAG Engine]: Successfully indexed '{file_name}' into project '{project_name}'.")
        return True
    except Exception as e:
        print(f"[RAG Engine Error]: Ingestion processing failed: {e}")
        return False


def query_vector_store(query, project_name, pdf_name=None):

    if pdf_name:
        doc_filter = {
            "$and": [
                {"project": {"$eq": project_name}},
                {"source": {"$eq": pdf_name}}
            ]
        }
        print(f"[RAG Engine]: Searching inside file '{pdf_name}'...")
    else:
        doc_filter = {"project": {"$eq": project_name}}
        print(f"[RAG Engine]: Searching globally across all project assets...")

    retrieved_docs = vector_store.similarity_search(query, k=5, filter=doc_filter)

    if not retrieved_docs:
        print("[RAG Engine]: No relevant information matches the specified tracking criteria.")
        return

    context_text = "\n\n".join([doc.page_content for doc in retrieved_docs])

    prompt = ChatPromptTemplate.from_messages([
        (
            "system",
            "You are an AI assistant. Answer the user's question using ONLY the "
            "context fragments provided below. If the answer is not in the context, "
            "say so clearly.\n\nContext:\n{context}"
        ),
        ("human", "{question}")
    ])

    chain = prompt | llm
    print("Processing answer...")
    response = chain.invoke({"context": context_text, "question": query})

    print("\nANSWER:")
    print(response.content)
    print("\n")


def delete_project_embeddings(project_name):
    try:
        vector_store._collection.delete(where={"project": {"$eq": project_name}})
        print(f"[RAG Engine]: Dropped all vector store embeddings for project '{project_name}'.")
    except Exception as e:
        print(f"[RAG Engine Error]: Failed to drop project vector assets: {e}")


def delete_pdf_embeddings(project_name, pdf_name):
    try:
        vector_store._collection.delete(
            where={
                "$and": [
                    {"project": {"$eq": project_name}},
                    {"source": {"$eq": pdf_name}}
                ]
            }
        )
        print(f"[RAG Engine]: Dropped vector store embeddings for file '{pdf_name}' inside '{project_name}'.")
    except Exception as e:
        print(f"[RAG Engine Error]: Failed to drop targeted file vector assets: {e}")
