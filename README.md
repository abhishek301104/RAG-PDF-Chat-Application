# RAG-Based PDF Chat Application

🔗 **Live Demo:** [Try the RAG-Based PDF Chat Application](https://rag-pdf-chat-application-h5cxmzumrxnqbn7nd8zvvw.streamlit.app/)

A beginner-friendly Retrieval-Augmented Generation (RAG) application that allows users to upload PDFs and ask questions about their content using AI.

## Technologies Used

- Python
- Streamlit
- LangChain Text Splitter
- FAISS Vector Search
- Google Gemini API
- Gemini Embeddings

## Architecture

```text
PDF
 |
Text Extraction
 |
Chunking
 |
Embeddings
 |
FAISS Index
 |
User Question
 |
Query Embedding
 |
Similarity Search (Top-K Chunks)
 |
Gemini Prompt
 |
AI-Generated Answer
```

## Setup

### 1. Create a Virtual Environment

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

### 2. Install Packages

```powershell
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### 3. Configure Your Gemini API Key

Copy `.env.example` to `.env` and add your API key:

```text
GEMINI_API_KEY=your_real_key
```

If needed, add the following lines at the top of `app.py` to load environment variables:

```python
from dotenv import load_dotenv
load_dotenv()
```

### 4. Run the Application

```powershell
streamlit run app.py
```

Open the local URL provided by Streamlit, usually:

http://localhost:8501

## Important Notes

- The FAISS index is built in memory and is not saved to disk.
- Scanned or image-only PDFs may require OCR to extract text.
- Never commit your `.env` file or expose your Gemini API key.

## Future Improvements

- Add OCR support for scanned PDFs.
- Save and reuse FAISS indexes.
- Improve document processing and error handling.
- Add support for multiple PDF documents.

## Author

Developed as a Python and Generative AI project to explore Retrieval-Augmented Generation, semantic search, and document question answering.
