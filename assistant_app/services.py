import os, re
from pathlib import Path
import chromadb
import requests
from django.conf import settings
from pypdf import PdfReader
from sentence_transformers import SentenceTransformer
CHROMA_PATH = settings.BASE_DIR / "chroma_db"
_embedding_model = None
_chroma_client = None
def get_embedding_model():
    global _embedding_model
    if _embedding_model is None:
        _embedding_model = SentenceTransformer(os.getenv("EMBEDDING_MODEL", "sentence-transformers/all-MiniLM-L6-v2"))
    return _embedding_model
def get_chroma_client():
    global _chroma_client
    if _chroma_client is None:
        CHROMA_PATH.mkdir(parents=True, exist_ok=True)
        _chroma_client = chromadb.PersistentClient(path=str(CHROMA_PATH))
    return _chroma_client
def collection_name(user_id): return f"studymate_user_{int(user_id)}"
def extract_text(file_path):
    path = Path(file_path)
    if path.suffix.lower() == ".txt": return path.read_text(encoding="utf-8", errors="replace")
    if path.suffix.lower() == ".pdf":
        reader = PdfReader(str(path)); pages = []
        for number, page in enumerate(reader.pages, start=1):
            content = (page.extract_text() or "").strip()
            if content: pages.append(f"[Page {number}]\n{content}")
        return "\n\n".join(pages)
    raise ValueError("Only PDF and TXT files are supported.")
def split_text(text, size=900, overlap=150):
    text = re.sub(r"[ \t]+", " ", text).strip()
    chunks=[]; start=0
    while start < len(text):
        end=min(start+size, len(text))
        if end < len(text):
            boundary=text.rfind(" ", start+int(size*.65), end)
            if boundary > start: end=boundary
        piece=text[start:end].strip()
        if piece: chunks.append(piece)
        if end >= len(text): break
        start=max(end-overlap, start+1)
    return chunks
def index_document(user_id, document_id, file_path):
    chunks=split_text(extract_text(file_path), int(os.getenv("CHUNK_SIZE", "900")), int(os.getenv("CHUNK_OVERLAP", "150")))
    if not chunks: raise ValueError("No readable text found. Scanned PDFs need OCR first.")
    collection=get_chroma_client().get_or_create_collection(name=collection_name(user_id), metadata={"hnsw:space":"cosine"})
    vectors=get_embedding_model().encode(chunks, normalize_embeddings=True).tolist()
    ids=[f"doc{document_id}_chunk{i}" for i in range(len(chunks))]
    metadata=[{"document_id":int(document_id), "chunk_index":i, "source":Path(file_path).name} for i in range(len(chunks))]
    collection.add(ids=ids, documents=chunks, embeddings=vectors, metadatas=metadata)
    return len(chunks)
def remove_document_chunks(user_id, document_id):
    try: get_chroma_client().get_collection(collection_name(user_id)).delete(where={"document_id":int(document_id)})
    except Exception: pass
def retrieve_context(user_id, question):
    try: collection=get_chroma_client().get_collection(collection_name(user_id))
    except Exception: return []
    if collection.count() == 0: return []
    count=min(int(os.getenv("RAG_TOP_K", "4")), collection.count())
    vector=get_embedding_model().encode([question], normalize_embeddings=True).tolist()
    result=collection.query(query_embeddings=vector, n_results=count, include=["documents", "metadatas", "distances"])
    docs=(result.get("documents") or [[]])[0]; metas=(result.get("metadatas") or [[]])[0]; distances=(result.get("distances") or [[]])[0]
    return [{"text":d, "source":m.get("source", "uploaded notes"), "distance":dist} for d,m,dist in zip(docs,metas,distances)]
def ollama_chat(messages):
    base=os.getenv("OLLAMA_BASE_URL", "http://localhost:11434").rstrip("/"); model=os.getenv("OLLAMA_MODEL", "llama3.2:3b")
    try:
        response=requests.post(f"{base}/api/chat", json={"model":model, "messages":messages, "stream":False}, timeout=180)
        response.raise_for_status()
        answer=response.json().get("message", {}).get("content", "").strip()
        if not answer: raise RuntimeError("Ollama returned an empty answer.")
        return answer
    except requests.exceptions.ConnectionError as exc: raise RuntimeError(f"Cannot connect to Ollama at {base}. Start Ollama and run: ollama pull {model}") from exc
    except requests.exceptions.Timeout as exc: raise RuntimeError("Ollama timed out. Try a smaller model or shorter question.") from exc
    except requests.exceptions.HTTPError as exc:
        detail=response.text[:300]
        if response.status_code == 404: raise RuntimeError(f"Model '{model}' was not found. Run: ollama pull {model}") from exc
        raise RuntimeError(f"Ollama error {response.status_code}: {detail}") from exc
def answer_question(user_id, question, history=None):
    matches=retrieve_context(user_id, question)
    if matches:
        context="\n\n".join(f"[Source: {m['source']}]\n{m['text']}" for m in matches)
        system=("You are StudyMate AI, a friendly tutor. Explain in simple English. For coding, give correct code and explain the key lines. Use retrieved notes when relevant. If the answer is not in the notes, clearly say so before giving general knowledge. Do not invent document facts.\n\nRetrieved notes:\n"+context)
    else:
        system="You are StudyMate AI, a friendly tutor for study and programming questions. Explain in simple English with examples. Give code and a short explanation when useful. No relevant uploaded-note chunks were retrieved; do not pretend to have read notes."
    messages=[{"role":"system", "content":system}]
    for item in (history or [])[-8:]:
        if item.get("role") in {"user", "assistant"} and item.get("content"): messages.append({"role":item["role"], "content":item["content"][:5000]})
    messages.append({"role":"user", "content":question})
    return ollama_chat(messages), matches
