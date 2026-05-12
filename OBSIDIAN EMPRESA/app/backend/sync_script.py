import hashlib
import json
import os
import re
from pathlib import Path

from dotenv import load_dotenv
from openai import OpenAI
from sqlalchemy.orm import Session

from database import Document, DocumentChunk, SessionLocal, init_db
from github_repo import ensure_content_repo
from settings import settings

load_dotenv()

openai_client = OpenAI(api_key=settings.openai_api_key)

# Regex para achar [[links]] e #tags
WIKI_LINK_PATTERN = re.compile(r"\[\[(.*?)\]\]")
TAG_PATTERN = re.compile(r"(?<!#)#([a-zA-Z0-9_\-]+)")


def parse_markdown_file(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    links = WIKI_LINK_PATTERN.findall(content)
    tags = TAG_PATTERN.findall(content)

    return content, {"links": list(set(links)), "tags": list(set(tags))}


def get_embedding(text):
    if not text.strip():
        return None
    try:
        response = openai_client.embeddings.create(
            input=text,
            model=settings.embedding_model,
        )
        return response.data[0].embedding
    except Exception as e:
        print(f"Erro ao gerar embedding: {e}")
        return None


def chunk_text(text, max_chars=1000, overlap=100):
    chunks = []
    start = 0
    text_len = len(text)
    while start < text_len:
        end = min(start + max_chars, text_len)
        if end < text_len:
            last_space = text.rfind(" ", start, end)
            if last_space != -1 and last_space > start + max_chars / 2:
                end = last_space
        chunks.append(text[start:end])
        start = max(0, end - overlap)
        if end >= text_len:
            break
    return chunks


def _sha1(text):
    return hashlib.sha1(text.encode("utf-8")).hexdigest()


def _md5(text):
    return hashlib.md5(text.encode("utf-8")).hexdigest()


def _guess_vault(rel_path):
    parts = Path(rel_path).parts
    return parts[0] if parts else "ROOT"


def sync_vaults(root_dir):
    print("Iniciando sincronização...")
    db: Session = SessionLocal()

    root_dir = os.path.abspath(root_dir)
    source_repo = settings.github_repo_url or "local"

    for dirpath, dirnames, filenames in os.walk(root_dir):
        dirnames[:] = [d for d in dirnames if not d.startswith(".")]

        for filename in filenames:
            if not filename.endswith(".md"):
                continue

            filepath = os.path.join(dirpath, filename)
            rel_path = os.path.relpath(filepath, root_dir)
            print(f"Processando: {rel_path}...")

            content, metadata = parse_markdown_file(filepath)
            content_hash = _sha1(content)
            document_id = _sha1(f"{source_repo}:{rel_path}")
            vault_name = _guess_vault(rel_path)
            title = os.path.splitext(os.path.basename(rel_path))[0]

            existing_document = db.query(Document).filter(Document.id == document_id).first()
            if existing_document and existing_document.content_hash == content_hash:
                continue

            db.query(DocumentChunk).filter(DocumentChunk.document_id == document_id).delete(
                synchronize_session=False
            )

            document = existing_document or Document(
                id=document_id,
                source_repo=source_repo,
                filepath=rel_path,
                vault=vault_name,
                title=title,
                content_hash=content_hash,
                metadata_json=json.dumps(metadata),
            )
            document.source_repo = source_repo
            document.filepath = rel_path
            document.vault = vault_name
            document.title = title
            document.content_hash = content_hash
            document.metadata_json = json.dumps(metadata)

            if not existing_document:
                db.add(document)

            chunks = chunk_text(content)
            for idx, chunk_text_content in enumerate(chunks):
                chunk_content_hash = _sha1(chunk_text_content)
                chunk_id = _md5(f"{document_id}:{idx}:{chunk_content_hash}")
                embedding = get_embedding(chunk_text_content)
                if not embedding:
                    continue

                doc_chunk = DocumentChunk(
                    id=chunk_id,
                    document_id=document_id,
                    content_hash=chunk_content_hash,
                    vault=vault_name,
                    filepath=rel_path,
                    content=chunk_text_content,
                    metadata_json=json.dumps(metadata),
                    embedding=embedding,
                )
                db.add(doc_chunk)

            db.commit()

    print("Sincronização concluída!")


if __name__ == "__main__":
    init_db()
    if settings.github_repo_url:
        root_directory = ensure_content_repo()
    else:
        root_directory = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
    sync_vaults(root_directory)
