from dotenv import load_dotenv
load_dotenv()

import streamlit as st
from rag_pipeline import PDFRAG

st.set_page_config(page_title="RAG PDF Chat", page_icon="📚", layout="wide")

st.title("📚 RAG-Based PDF Chat Application")
st.caption("Ask questions about your PDF using semantic search + Google Gemini.")

if "rag" not in st.session_state:
    st.session_state.rag = None
if "messages" not in st.session_state:
    st.session_state.messages = []

with st.sidebar:
    st.header("1. Upload PDF")
    uploaded_file = st.file_uploader("Choose a PDF", type=["pdf"])

    chunk_size = st.slider("Chunk size", 500, 2000, 1000, 100)
    chunk_overlap = st.slider("Chunk overlap", 50, 400, 150, 50)
    top_k = st.slider("Top-K retrieved chunks", 2, 8, 4)

    if uploaded_file and st.button("Build knowledge base", type="primary"):
        with st.spinner("Reading PDF, creating chunks and FAISS index..."):
            try:
                pdf_bytes = uploaded_file.getvalue()
                st.session_state.rag = PDFRAG(
                    chunk_size=chunk_size,
                    chunk_overlap=chunk_overlap,
                    top_k=top_k,
                )
                info = st.session_state.rag.build_index(pdf_bytes, uploaded_file.name)
                st.session_state.messages = []
                st.success(
                    f"Indexed {info['chunks']} chunks from {info['pages']} pages."
                )
            except Exception as e:
                st.session_state.rag = None
                st.error(f"Could not index PDF: {e}")

    if st.session_state.rag:
        st.success("Knowledge base ready ✅")
        st.write(f"**Chunks:** {len(st.session_state.rag.chunks)}")

st.subheader("2. Chat with your document")

if not st.session_state.rag:
    st.info("Upload a PDF and click **Build knowledge base** to start.")
else:
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    question = st.chat_input("Ask something about your PDF...")
    if question:
        st.session_state.messages.append({"role": "user", "content": question})
        with st.chat_message("user"):
            st.markdown(question)

        with st.chat_message("assistant"):
            with st.spinner("Searching the PDF and generating an answer..."):
                try:
                    answer, sources = st.session_state.rag.answer(
                        question, st.session_state.messages[:-1]
                    )
                    st.markdown(answer)

                    with st.expander("🔎 Retrieved context"):
                        for i, source in enumerate(sources, 1):
                            st.markdown(
                                f"**Chunk {i} — page {source['page']}**\n\n"
                                f"{source['text'][:1200]}"
                            )

                    st.session_state.messages.append(
                        {"role": "assistant", "content": answer}
                    )
                except Exception as e:
                    st.error(f"Error: {e}")
