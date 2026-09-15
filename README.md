# RAG-Based PDF Chat Application

A beginner-friendly Retrieval-Augmented Generation application built with:

- Python
- Streamlit
- LangChain Text Splitter
- FAISS vector search
- Google Gemini API
- Gemini embeddings

## Architecture

PDF -> Text extraction -> Chunking -> Embeddings -> FAISS index
                                              |
User question -> Query embedding -> Similarity search -> Top-K chunks
                                              |
                                      Gemini prompt
                                              |
                                           Answer

## Setup

### 1. Create a virtual environment

Windows PowerShell:

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
```

If PowerShell blocks activation:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\.venv\Scripts\Activate.ps1
```

### 2. Install packages

```powershell
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### 3. Add your Gemini API key

Copy `.env.example` to `.env`:

```text
GEMINI_API_KEY=your_real_key
```

The app reads the key from the environment. Because the project uses `python-dotenv`, add this line at the top of `app.py` if your environment does not load `.env` automatically:

```python
from dotenv import load_dotenv
load_dotenv()
```

### 4. Run

```powershell
streamlit run app.py
```

Open the local URL shown by Streamlit, normally:

```text
http://localhost:8501
```

## Important

This version builds the FAISS index in memory. It does not save the index to disk.

For scanned/image-only PDFs, text extraction may return little or no text. OCR can be added later.

Do not commit `.env` or expose your Gemini API key.
