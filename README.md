# 📚 Multi-Project Local RAG Agent

A fully offline, multi-project Retrieval-Augmented Generation (RAG) system that lets you upload PDF documents, organize them into projects, and ask questions — all running locally using **Ollama** with no API keys or internet required.

---

## 🗂️ Project Structure

```
RAG_Agent/
│
├── main.py              # CLI interface — all user interaction
├── rag_app.py           # RAG engine — ingestion, querying, deletion
├── helpers.py           # File system utilities
├── requirements.txt     # Python dependencies
│
├── data/                # Stores staged PDF copies per project
│   └── <project_name>/
│       └── <file.pdf>
│
└── chroma_db/           # Chroma vector database (auto-created)
```

---

## ⚙️ Prerequisites

- Python 3.9+
- [Ollama](https://ollama.com/download) installed and running

---

## 🚀 Setup & Installation

### 1. Install Ollama

**Windows:** Download and run the installer from [ollama.com/download](https://ollama.com/download)

**Linux/macOS:**
```bash
curl -fsSL https://ollama.com/install.sh | sh
```

### 2. Pull the Required Models

Open a terminal and run:

```bash
ollama pull nomic-embed-text   # Embedding model (~274MB)
ollama pull llama3.2           # LLM for answering (~2GB)
```

> **Low RAM (< 8GB)?** Use a lighter LLM instead:
> ```bash
> ollama pull qwen2.5:0.5b
> ```
> Then set `LLM_MODEL = "qwen2.5:0.5b"` in `rag_app.py`.

### 3. Clone / Download the Project

```bash
cd your-project-folder
```

### 4. Create a Virtual Environment (Recommended)

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/macOS
source venv/bin/activate
```

### 5. Install Python Dependencies

```bash
pip install -r requirements.txt
```

### 6. Run the App

```bash
python main.py
```

---

## 🖥️ Usage

The app runs as an interactive CLI menu with 6 options:

```
📚 Multi-Project Interactive RAG Interface Environment
====================================================
 1. Create a New Project Workspace
 2. Ingest / Upload a PDF Document
 3. Ask Questions (Mandatory Project Filter Scope)
 4. Delete Data Assets (Project or Specific PDF Source)
 5. Inspect Active Catalog Assets Index Tree
 6. Exit Environment Framework
```

### Typical Workflow

**Step 1 — Create a project**
Select option `1` and give it a name (e.g. `physics`, `legal_docs`).

**Step 2 — Upload a PDF**
Select option `2`, choose your project, then paste the full path to your PDF:
```
D:\Documents\my_file.pdf
```

**Step 3 — Ask questions**
Select option `3`, choose your project, then either:
- Query all PDFs in the project at once
- Filter to a single specific PDF

**Step 4 — Manage data**
Select option `4` to delete an entire project or a single PDF (removes both the file and its vectors from the database).

**Step 5 — Inspect catalog**
Select option `5` to see all projects and their uploaded PDFs.

---

## 🔧 Configuration

All model settings are at the top of `rag_app.py`:

```python
EMBED_MODEL = "nomic-embed-text"   # Embedding model (don't change unless re-ingesting all PDFs)
LLM_MODEL   = "llama3.2"           # LLM for answering questions
```

To switch the LLM, pull the new model with Ollama and update `LLM_MODEL`. The embedding model should stay consistent — changing it requires wiping `chroma_db/` and re-ingesting all PDFs.

---

## 📦 Dependencies

| Package | Purpose |
|---|---|
| `langchain` | Core RAG orchestration |
| `langchain-ollama` | Ollama LLM + embeddings integration |
| `langchain-chroma` | Chroma vector store integration |
| `langchain-community` | PDF document loader |
| `langchain-text-splitters` | Document chunking |
| `pypdf` | PDF parsing |
| `python-dotenv` | Environment variable loading |

---

## 🧠 How It Works

```
PDF File
   │
   ▼
PyPDFLoader → raw text pages
   │
   ▼
RecursiveCharacterTextSplitter → chunks (1000 chars, 200 overlap)
   │
   ▼
OllamaEmbeddings (nomic-embed-text) → vector embeddings
   │
   ▼
Chroma Vector DB (persisted locally in chroma_db/)
   │
   ▼ (on query)
similarity_search (top 5 chunks) → context
   │
   ▼
ChatOllama (llama3.2) + prompt → Answer
```

Each chunk is tagged with `project` and `source` metadata so queries can be scoped to a specific project or file.

---

## ❗ Troubleshooting

| Problem | Fix |
|---|---|
| `ollama` not recognized in terminal | Restart terminal or PC after installing Ollama |
| `model requires more system memory` | Close other apps to free RAM, or switch to `qwen2.5:0.5b` |
| `localhost:11434` not responding | Open Ollama from system tray or run `ollama serve` |
| No results returned from query | Make sure the PDF was ingested successfully first |
| Changing embedding model breaks queries | Delete `chroma_db/` folder and re-ingest all PDFs |

---

## 📝 Notes

- The `data/` folder stores local copies of your PDFs — the originals are not moved or modified.
- The `chroma_db/` folder is the vector database — do not manually edit it.
- All processing is 100% local. No data leaves your machine.