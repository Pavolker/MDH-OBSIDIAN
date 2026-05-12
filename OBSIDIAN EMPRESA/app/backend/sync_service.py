import hashlib
import hmac
import json
import uuid
from datetime import datetime
from typing import Optional

from fastapi import HTTPException

from database import SessionLocal, SyncJob
from github_repo import ensure_content_repo
from settings import settings
from sync_script import sync_vaults


def create_sync_job(source_repo: str) -> str:
    job_id = uuid.uuid4().hex
    db = SessionLocal()
    try:
        job = SyncJob(id=job_id, source_repo=source_repo, status="running")
        db.add(job)
        db.commit()
        return job_id
    finally:
        db.close()


def _update_job(job_id: str, status: str, error_message: Optional[str] = None):
    db = SessionLocal()
    try:
        job = db.query(SyncJob).filter(SyncJob.id == job_id).first()
        if not job:
            return
        job.status = status
        job.finished_at = datetime.utcnow()
        job.error_message = error_message
        db.commit()
    finally:
        db.close()


def execute_sync_job(job_id: str):
    if not settings.github_repo_url:
        raise HTTPException(status_code=400, detail="GITHUB_REPO_URL não configurada.")

    try:
        root_directory = ensure_content_repo()
        sync_vaults(root_directory)
        _update_job(job_id, "completed")
    except Exception as exc:
        _update_job(job_id, "failed", str(exc))
        raise


def verify_github_signature(payload_bytes: bytes, signature_header: Optional[str]):
    secret = settings.github_webhook_secret
    if not secret:
        raise HTTPException(status_code=400, detail="GITHUB_WEBHOOK_SECRET não configurado.")
    if not signature_header or not signature_header.startswith("sha256="):
        raise HTTPException(status_code=401, detail="Assinatura ausente.")

    expected = hmac.new(
        secret.encode("utf-8"),
        payload_bytes,
        hashlib.sha256,
    ).hexdigest()
    received = signature_header.split("sha256=", 1)[1]
    if not hmac.compare_digest(expected, received):
        raise HTTPException(status_code=401, detail="Assinatura inválida.")


def parse_github_event(event_name: Optional[str], payload_bytes: bytes):
    if event_name and event_name != "push":
        return None
    return json.loads(payload_bytes.decode("utf-8"))
