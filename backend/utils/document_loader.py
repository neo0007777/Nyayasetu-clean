import os
from pathlib import Path
from striprtf.striprtf import rtf_to_text
from docx import Document


def load_rtf(filepath: str) -> str:
    with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
        raw = f.read()
    return rtf_to_text(raw).strip()


def load_docx(filepath: str) -> str:
    doc = Document(filepath)
    return "\n".join(
        p.text.strip() for p in doc.paragraphs if p.text.strip()
    )


def load_document(filepath: str) -> str:
    ext = Path(filepath).suffix.lower()
    if ext == ".rtf":
        return load_rtf(filepath)
    elif ext == ".docx":
        return load_docx(filepath)
    return ""


def load_all_documents(data_dir: str) -> list:
    documents = []
    data_path = Path(data_dir)

    if not data_path.exists():
        print(f"[Loader] Directory not found: {data_dir}")
        return documents

    supported = {".rtf", ".docx"}
    all_files = [f for f in data_path.rglob("*") if f.suffix.lower() in supported]
    print(f"[Loader] Found {len(all_files)} files in {data_dir}")

    for filepath in all_files:
        try:
            text = load_document(str(filepath))
            if not text or len(text) < 50:
                continue
            documents.append({
                "text": text,
                "metadata": {
                    "filename": filepath.name,
                    "category": filepath.parent.name,
                    "filepath": str(filepath),
                }
            })
        except Exception as e:
            print(f"[Loader] Skipping {filepath.name}: {e}")

    print(f"[Loader] Loaded {len(documents)} documents successfully")
    return documents
