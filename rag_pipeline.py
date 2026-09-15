import io
import os
import numpy as np
import faiss
from pypdf import PdfReader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from google import genai
from google.genai import types


class PDFRAG:
    def __init__(self, chunk_size=1000, chunk_overlap=150, top_k=4):
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError(
                "GEMINI_API_KEY is missing. Add it to your .env file and restart Streamlit."
            )

        self.client = genai.Client(api_key=api_key)
        self.embedding_model = "gemini-embedding-001"
        self.generation_model ="gemini-3.6-flash"
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.top_k = top_k
        self.index = None
        self.chunks = []

    def _embed(self, texts):
        vectors = []
        for text in texts:
            result = self.client.models.embed_content(
                model=self.embedding_model,
                contents=text,
                config=types.EmbedContentConfig(output_dimensionality=768),
            )
            vectors.append(result.embeddings[0].values)

        matrix = np.asarray(vectors, dtype="float32")
        faiss.normalize_L2(matrix)
        return matrix

    def build_index(self, pdf_bytes, filename="document.pdf"):
        reader = PdfReader(io.BytesIO(pdf_bytes))
        splitter = RecursiveCharacterTextSplitter(
            chunk_size=self.chunk_size,
            chunk_overlap=self.chunk_overlap,
            separators=["\n\n", "\n", ". ", " ", ""],
        )

        chunks = []
        for page_number, page in enumerate(reader.pages, start=1):
            text = page.extract_text() or ""
            text = text.strip()
            if not text:
                continue

            for chunk in splitter.split_text(text):
                chunks.append(
                    {
                        "text": chunk,
                        "page": page_number,
                        "source": filename,
                    }
                )

        if not chunks:
            raise ValueError(
                "No readable text was found. If this is a scanned/image-only PDF, OCR is required."
            )

        self.chunks = chunks
        embeddings = self._embed([c["text"] for c in chunks])

        self.index = faiss.IndexFlatIP(embeddings.shape[1])
        self.index.add(embeddings)

        return {"pages": len(reader.pages), "chunks": len(chunks)}

    def retrieve(self, question):
        query_vector = self._embed([question])
        scores, indices = self.index.search(
            query_vector, min(self.top_k, len(self.chunks))
        )

        results = []
        for score, idx in zip(scores[0], indices[0]):
            if idx == -1:
                continue
            item = dict(self.chunks[int(idx)])
            item["score"] = float(score)
            results.append(item)
        return results

    def answer(self, question, history=None):
        results = self.retrieve(question)

        context_parts = []
        for item in results:
            context_parts.append(
                f"[Page {item['page']}]\n{item['text']}"
            )
        context = "\n\n---\n\n".join(context_parts)

        recent_history = ""
        if history:
            recent = history[-6:]
            recent_history = "\n".join(
                f"{m['role'].upper()}: {m['content']}" for m in recent
            )

        prompt = f"""
You are a PDF question-answering assistant.

Answer the user's question using ONLY the retrieved PDF context below.
If the answer is not present in the context, clearly say:
"I couldn't find that information in the uploaded PDF."

Do not invent facts. Keep the answer clear and interview-friendly.
Mention page numbers when useful.

Conversation history:
{recent_history}

Retrieved PDF context:
{context}

User question:
{question}
"""

        response = self.client.models.generate_content(
            model=self.generation_model,
            contents=prompt,
            config=types.GenerateContentConfig(
                temperature=0.2,
                max_output_tokens=800,
            ),
        )

        return response.text, results
