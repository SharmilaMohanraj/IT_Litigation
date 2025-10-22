from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

class DocumentStatus(BaseModel):
    status_id: str = Field(..., description="Status identifier (DR, E, P, C)")
    message: str = Field(..., description="Status message description")

class DocumentSession(BaseModel):
    PID: str = Field(..., description="Process ID (UUID)")
    status: DocumentStatus

class AuditLogsBase(BaseModel):
    filename: str = Field(..., description="Document filename")
    session: DocumentSession

class AuditLogsCreate(AuditLogsBase):
    pass

class AuditLogs(AuditLogsBase):
    id: str
    created_at: datetime
    updated_at: datetime

class AuditLogsUpdate(BaseModel):
    filename: Optional[str] = None
    session: Optional[DocumentSession] = None

# Statistics and Analytics Schemas
class DocumentStatusStats(BaseModel):
    total_documents: int
    status_breakdown: dict
    recent_documents_24h: int
    status_descriptions: dict

class AuditLogsStats(BaseModel):
    total_documents: int
    documents_by_status: dict
    recent_activity: int
    average_processing_time: Optional[float] = None

# Error Response Schema
class ErrorResponse(BaseModel):
    error: str
    detail: Optional[str] = None
    timestamp: datetime = Field(default_factory=datetime.now)
