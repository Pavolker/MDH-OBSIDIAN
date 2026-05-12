#!/usr/bin/env python3
"""
Script para indexar vaults Obsidian locais no banco de dados
"""
import os
import sys
import hashlib
import uuid
from pathlib import Path
from datetime import datetime

# Adiciona o backend ao path
backend_path = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, backend_path)

from database import init_db, SessionLocal, Document, DocumentChunk
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

# Configuração OpenAI
openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "text-embedding-3-small")

def get_embedding(text):
    """Gera embedding para o texto"""
    try:
        response = openai_client.embeddings.create(
            input=text[:8000],  # Limita tamanho
            model=EMBEDDING_MODEL,
        )
        return response.data[0].embedding
    except Exception as e:
        print(f"Erro ao gerar embedding: {e}")
        return None

def parse_metadata(content, filepath):
    """Extrai metadata do conteúdo markdown"""
    metadata = {
        "tags": [],
        "links": []
    }
    
    # Extrai tags (#tag)
    import re
    tags = re.findall(r'#(\w+)', content)
    metadata["tags"] = list(set(tags))
    
    # Extrai links [[wiki-links]]
    links = re.findall(r'\[\[([^\]]+)\]\]', content)
    metadata["links"] = list(set(links))
    
    # Extrai título do primeiro heading
    title_match = re.search(r'^#\s+(.+)$', content, re.MULTILINE)
    if title_match:
        metadata["title"] = title_match.group(1).strip()
    
    return metadata

def chunk_content(content, chunk_size=1000):
    """Divide conteúdo em chunks"""
    chunks = []
    paragraphs = content.split('\n\n')
    current_chunk = ""
    
    for para in paragraphs:
        if len(current_chunk) + len(para) < chunk_size:
            current_chunk += para + '\n\n'
        else:
            if current_chunk:
                chunks.append(current_chunk.strip())
            current_chunk = para + '\n\n'
    
    if current_chunk:
        chunks.append(current_chunk.strip())
    
    return chunks if chunks else [content[:chunk_size]]

def index_vault(vault_path, vault_name):
    """Indexa um vault Obsidian"""
    print(f"\n📚 Indexando vault: {vault_name}")
    print(f"📁 Path: {vault_path}\n")
    
    db = SessionLocal()
    indexed_count = 0
    error_count = 0
    
    try:
        # Encontra todos os arquivos .md
        md_files = list(Path(vault_path).rglob("*.md"))
        print(f"Encontrados {len(md_files)} arquivos markdown\n")
        
        for md_file in md_files:
            try:
                # Pula pastas do Obsidian
                if '.obsidian' in str(md_file):
                    continue
                
                # Lê o conteúdo
                content = md_file.read_text(encoding='utf-8')
                if not content.strip():
                    continue
                
                # Gera ID único baseado no path
                filepath = str(md_file.relative_to(vault_path))
                doc_id = hashlib.sha256(f"{vault_name}:{filepath}".encode()).hexdigest()
                content_hash = hashlib.sha256(content.encode()).hexdigest()
                
                # Verifica se já existe
                existing = db.query(Document).filter(Document.id == doc_id).first()
                if existing and existing.content_hash == content_hash:
                    print(f"⏭️  Skip: {filepath} (já indexado)")
                    continue
                
                # Parse metadata
                metadata = parse_metadata(content, filepath)
                
                # Cria ou atualiza documento
                if existing:
                    existing.content_hash = content_hash
                    existing.title = metadata.get("title", filepath)
                    existing.metadata_json = str(metadata)
                    existing.last_indexed_at = datetime.utcnow()
                else:
                    doc = Document(
                        id=doc_id,
                        source_repo="local",
                        filepath=filepath,
                        vault=vault_name,
                        title=metadata.get("title", filepath),
                        content_hash=content_hash,
                        metadata_json=str(metadata),
                        last_indexed_at=datetime.utcnow()
                    )
                    db.add(doc)
                
                # Cria chunks com embeddings
                chunks = chunk_content(content)
                for i, chunk_text in enumerate(chunks):
                    chunk_id = hashlib.sha256(f"{doc_id}:chunk{i}".encode()).hexdigest()
                    
                    # Remove chunk antigo se existir
                    db.query(DocumentChunk).filter(DocumentChunk.id == chunk_id).delete()
                    
                    # Gera embedding
                    embedding = get_embedding(chunk_text)
                    if embedding is None:
                        continue
                    
                    chunk = DocumentChunk(
                        id=chunk_id,
                        document_id=doc_id,
                        content_hash=content_hash,
                        vault=vault_name,
                        filepath=filepath,
                        content=chunk_text,
                        metadata_json=str(metadata),
                        embedding=embedding
                    )
                    db.add(chunk)
                
                db.commit()
                indexed_count += 1
                print(f"✅ Indexed: {filepath}")
                
            except Exception as e:
                error_count += 1
                print(f"❌ Error em {md_file}: {e}")
                db.rollback()
                continue
        
        print(f"\n✨ Indexação completa!")
        print(f"   ✅ Sucesso: {indexed_count} arquivos")
        print(f"   ❌ Erros: {error_count} arquivos")
        
    finally:
        db.close()

if __name__ == "__main__":
    # Inicializa o banco
    print("🔧 Inicializando banco de dados...")
    init_db()
    
    # Lista de vaults para indexar
    vaults = [
        ("/Users/APLICATIVOS GERAIS/OBSIDIAN/DADOS", "DADOS"),
        # Adicione mais vaults conforme necessário:
        # ("/Users/APLICATIVOS GERAIS/OBSIDIAN/CENTAUR0", "CENTAURO"),
        # ("/Users/APLICATIVOS GERAIS/OBSIDIAN/CODEX", "CODEX"),
    ]
    
    for vault_path, vault_name in vaults:
        if os.path.exists(vault_path):
            index_vault(vault_path, vault_name)
        else:
            print(f"⚠️  Vault não encontrado: {vault_path}")
    
    print("\n🎉 Processo finalizado!")
    print("Agora você pode usar a busca no frontend!")
