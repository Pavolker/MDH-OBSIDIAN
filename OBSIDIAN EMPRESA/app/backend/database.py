import os
import json
from datetime import datetime
from sqlalchemy import create_engine, Column, String, Text, DateTime, text
from sqlalchemy.orm import declarative_base, sessionmaker
from pgvector.sqlalchemy import Vector
from settings import settings

# Usa a URL do banco de dados do settings
DATABASE_URL = settings.database_url
# Ajeita URL de postgres se vier apenas postgres://
if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

class DocumentChunk(Base):
    __tablename__ = "document_chunks"

    id = Column(String, primary_key=True, index=True) # Pode ser um hash do vault+filepath+chunk_index
    document_id = Column(String, index=True)
    content_hash = Column(String, index=True)
    vault = Column(String, index=True)
    filepath = Column(String, index=True)
    content = Column(Text)
    metadata_json = Column(Text) # Tags, links encontrados, etc
    embedding = Column(Vector(1536)) # Dimensionamento para text-embedding-3-small (OpenAI)

    @property
    def parsed_metadata(self):
        try:
            return json.loads(self.metadata_json) if self.metadata_json else {}
        except json.JSONDecodeError:
            return {}


class Document(Base):
    __tablename__ = "documents"

    id = Column(String, primary_key=True, index=True)
    source_repo = Column(String, index=True)
    filepath = Column(String, index=True, unique=True)
    vault = Column(String, index=True)
    title = Column(String, index=True)
    content_hash = Column(String, index=True)
    metadata_json = Column(Text)
    last_indexed_at = Column(DateTime, default=datetime.utcnow)

    @property
    def parsed_metadata(self):
        try:
            return json.loads(self.metadata_json) if self.metadata_json else {}
        except json.JSONDecodeError:
            return {}


class SyncJob(Base):
    __tablename__ = "sync_jobs"

    id = Column(String, primary_key=True, index=True)
    source_repo = Column(String, index=True)
    status = Column(String, index=True)
    started_at = Column(DateTime, default=datetime.utcnow)
    finished_at = Column(DateTime, nullable=True)
    error_message = Column(Text, nullable=True)

def init_db():
    # Garante que a extensao pgvector existe
    with engine.connect() as conn:
        conn.execute(text("CREATE EXTENSION IF NOT EXISTS vector"))
        conn.commit()
    Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
