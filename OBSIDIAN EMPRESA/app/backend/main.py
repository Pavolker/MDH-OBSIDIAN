from fastapi import FastAPI, Depends, HTTPException, Request, Header, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from pydantic import BaseModel
from openai import OpenAI
from typing import List, Optional

from database import get_db, Document, DocumentChunk, SyncJob, init_db
from sync_service import (
    create_sync_job,
    execute_sync_job,
    parse_github_event,
    verify_github_signature,
)
from settings import settings

app = FastAPI(title="O Cérebro Web API")

init_db()

allowed_origins = [settings.cors_origin] if settings.cors_origin != "*" else ["*"]

# Setup CORS para o frontend no Netlify poder conversar com a API
app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

openai_client = OpenAI(api_key=settings.openai_api_key)
openrouter_client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=settings.openrouter_api_key,
)

class SearchQuery(BaseModel):
    query: str
    limit: int = 5
    vault: Optional[str] = None

class ChatQuery(BaseModel):
    messages: List[dict] # [{role: "user", content: "..."}, ...]

def get_embedding(text_str):
    if not settings.openai_api_key:
        raise HTTPException(status_code=500, detail="OPENAI_API_KEY não configurada.")
    try:
        response = openai_client.embeddings.create(
            input=text_str,
            model=settings.embedding_model,
        )
        return response.data[0].embedding
    except Exception as e:
         raise HTTPException(status_code=500, detail="Erro no provedor de Embeddings AI")

@app.get("/")
def read_root():
    return {"status": "ok", "app": "O Cérebro Backend"}

@app.get("/health")
def health():
    return {"status": "healthy"}

@app.get("/api/stats")
def get_stats(db: Session = Depends(get_db)):
    total_chunks = db.query(DocumentChunk).count()
    total_documents = db.query(Document).count()
    total_vaults = len(
        [row[0] for row in db.query(Document.vault).distinct().all() if row[0]]
    )
    return {
        "total_chunks": total_chunks,
        "total_documents": total_documents,
        "total_vaults": total_vaults,
    }


@app.get("/api/vaults")
def list_vaults(db: Session = Depends(get_db)):
    vaults = [row[0] for row in db.query(Document.vault).distinct().order_by(Document.vault.asc()).all()]
    return {"vaults": vaults}


@app.get("/api/documents")
def list_documents(limit: int = 50, vault: Optional[str] = None, db: Session = Depends(get_db)):
    query = db.query(Document)
    if vault:
        query = query.filter(Document.vault == vault)
    documents = query.order_by(Document.last_indexed_at.desc()).limit(limit).all()
    return {
        "results": [
            {
                "id": doc.id,
                "filepath": doc.filepath,
                "vault": doc.vault,
                "title": doc.title,
                "metadata": doc.parsed_metadata,
                "last_indexed_at": doc.last_indexed_at.isoformat() if doc.last_indexed_at else None,
            }
            for doc in documents
        ]
    }


@app.get("/api/documents/{document_id}")
def get_document(document_id: str, db: Session = Depends(get_db)):
    doc = db.query(Document).filter(Document.id == document_id).first()
    if not doc:
        raise HTTPException(status_code=404, detail="Documento não encontrado.")

    chunks = (
        db.query(DocumentChunk)
        .filter(DocumentChunk.document_id == document_id)
        .order_by(DocumentChunk.id.asc())
        .all()
    )
    return {
        "id": doc.id,
        "filepath": doc.filepath,
        "vault": doc.vault,
        "title": doc.title,
        "metadata": doc.parsed_metadata,
        "chunks": [
            {
                "id": chunk.id,
                "content": chunk.content,
                "metadata": chunk.parsed_metadata,
            }
            for chunk in chunks
        ],
    }


@app.get("/api/documents/{document_id}/related")
def related_documents(document_id: str, limit: int = 8, db: Session = Depends(get_db)):
    doc = db.query(Document).filter(Document.id == document_id).first()
    if not doc:
        raise HTTPException(status_code=404, detail="Documento não encontrado.")

    metadata = doc.parsed_metadata
    doc_tags = set(metadata.get("tags", []))
    doc_links = set(metadata.get("links", []))
    doc_title = doc.title or ""
    doc_filepath = doc.filepath or ""

    documents = db.query(Document).filter(Document.id != document_id).all()
    scored = []

    for candidate in documents:
        candidate_metadata = candidate.parsed_metadata
        candidate_tags = set(candidate_metadata.get("tags", []))
        candidate_links = set(candidate_metadata.get("links", []))

        score = 0
        shared_tags = sorted(doc_tags.intersection(candidate_tags))
        shared_links = sorted(doc_links.intersection(candidate_links))

        if candidate.vault == doc.vault:
            score += 1
        score += len(shared_tags) * 3
        score += len(shared_links) * 2

        if doc_title and doc_title in candidate_links:
            score += 2
        if doc_filepath and doc_filepath in candidate_links:
            score += 4
        if candidate.title and candidate.title in doc_links:
            score += 2

        if score > 0:
            scored.append(
                {
                    "id": candidate.id,
                    "filepath": candidate.filepath,
                    "vault": candidate.vault,
                    "title": candidate.title,
                    "score": score,
                    "shared_tags": shared_tags,
                    "shared_links": shared_links,
                }
            )

    scored.sort(key=lambda item: item["score"], reverse=True)

    backlinks = []
    for candidate in documents:
        candidate_metadata = candidate.parsed_metadata
        candidate_links = set(candidate_metadata.get("links", []))
        if doc_title in candidate_links or doc_filepath in candidate_links:
            backlinks.append(
                {
                    "id": candidate.id,
                    "filepath": candidate.filepath,
                    "vault": candidate.vault,
                    "title": candidate.title,
                }
            )

    return {
        "related": scored[:limit],
        "backlinks": backlinks[:limit],
    }

@app.post("/api/search")
def search_notes(payload: SearchQuery, db: Session = Depends(get_db)):
    """Busca vetorial de notas"""
    query_emb = get_embedding(payload.query)
    
    # Busca com pgvector (usando L2 distance <->)
    query = db.query(DocumentChunk).order_by(DocumentChunk.embedding.l2_distance(query_emb))
    if payload.vault:
        query = query.filter(DocumentChunk.vault == payload.vault)
        
    results = query.limit(payload.limit).all()
    
    return {
        "results": [
            {
                "id": r.id, 
                "filepath": r.filepath, 
                "vault": r.vault,
                "content": r.content,
                "metadata": r.parsed_metadata,
                "distance": 0 # pgvector suporta extrair distancia mas simplificaremos pro MVP
            }
            for r in results
        ]
    }

@app.post("/api/chat")
def chat(payload: ChatQuery, db: Session = Depends(get_db)):
    """Endpoint simplificado para Chat/RAG"""
    # 1. Pega a ultima mensagem do usuario
    user_msgs = [m for m in payload.messages if m.get("role") == "user"]
    if not user_msgs:
        raise HTTPException(status_code=400, detail="Sem mensagens de usuario.")
        
    last_query = user_msgs[-1]["content"]
    
    # 2. Busca conteudo relevante
    query_emb = get_embedding(last_query)
    docs = db.query(DocumentChunk).order_by(DocumentChunk.embedding.l2_distance(query_emb)).limit(3).all()
    
    context = "\n\n---\n\n".join([f"Path: {d.filepath}\nContent:\n{d.content}" for d in docs])
    
    # 3. Chama AI para gerar resposta baseada no contexto
    system_prompt = (
        "Você é o assistente inteligente do 'O Cérebro', um segundo cérebro. "
        "Responda ao usuário utilizando o contexto a seguir que foi recuperado de suas anotações pessoais. "
        "Não invente respostas se não estiver no contexto.\n\n"
        f"CONTEXTO RECUPERADO:\n{context}"
    )
    
    messages = [{"role": "system", "content": system_prompt}] + payload.messages

    if not settings.openrouter_api_key:
        raise HTTPException(status_code=500, detail="OPENROUTER_API_KEY não configurada.")

    response = openrouter_client.chat.completions.create(
        model=settings.chat_model,
        messages=messages
    )
    
    return {"reply": response.choices[0].message.content, "sources": [d.filepath for d in docs]}


@app.post("/api/sync")
def trigger_sync():
    if not settings.github_repo_url:
        raise HTTPException(status_code=400, detail="GITHUB_REPO_URL não configurada.")

    job_id = create_sync_job(settings.github_repo_url)

    try:
        execute_sync_job(job_id)
        return {"job_id": job_id, "status": "completed"}
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Falha na sincronização: {exc}")


@app.get("/api/sync/jobs")
def list_sync_jobs(limit: int = 20, db: Session = Depends(get_db)):
    jobs = (
        db.query(SyncJob)
        .order_by(SyncJob.started_at.desc())
        .limit(limit)
        .all()
    )
    return {
        "results": [
            {
                "id": job.id,
                "source_repo": job.source_repo,
                "status": job.status,
                "started_at": job.started_at.isoformat() if job.started_at else None,
                "finished_at": job.finished_at.isoformat() if job.finished_at else None,
                "error_message": job.error_message,
            }
            for job in jobs
        ]
    }


@app.get("/api/sync/jobs/{job_id}")
def get_sync_job(job_id: str, db: Session = Depends(get_db)):
    job = db.query(SyncJob).filter(SyncJob.id == job_id).first()
    if not job:
        raise HTTPException(status_code=404, detail="Job não encontrado.")
    return {
        "id": job.id,
        "source_repo": job.source_repo,
        "status": job.status,
        "started_at": job.started_at.isoformat() if job.started_at else None,
        "finished_at": job.finished_at.isoformat() if job.finished_at else None,
        "error_message": job.error_message,
    }


@app.post("/api/webhooks/github")
async def github_webhook(
    request: Request,
    background_tasks: BackgroundTasks,
    x_github_event: Optional[str] = Header(default=None),
    x_hub_signature_256: Optional[str] = Header(default=None),
):
    payload_bytes = await request.body()
    verify_github_signature(payload_bytes, x_hub_signature_256)
    event = parse_github_event(x_github_event, payload_bytes)

    if event is None:
        return {"status": "ignored"}

    if not settings.github_repo_url:
        raise HTTPException(status_code=400, detail="GITHUB_REPO_URL não configurada.")

    job_id = create_sync_job(settings.github_repo_url)
    if background_tasks is not None:
        background_tasks.add_task(execute_sync_job, job_id)
    else:
        execute_sync_job(job_id)

    return {"status": "queued", "job_id": job_id}
