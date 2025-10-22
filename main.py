from fastapi import FastAPI, HTTPException, Depends, Query, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from database import (
    audit_logs_collection, 
    create_indexes, check_database_health
)
from models import (
    audit_logs_helper, 
)
from schemas import (
    AuditLogs, AuditLogsCreate,
    AuditLogsUpdate, DocumentStatusStats, ErrorResponse
)
from typing import List, Optional
from datetime import datetime
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI(
    title="IT Litigation System",
    description="Document processing and audit logging system based on collection.json structure",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Startup event
@app.on_event("startup")
async def startup_event():
    """Initialize database indexes on startup"""
    await create_indexes()
    logger.info("Application startup completed")

# Root endpoint
@app.get("/", response_model=dict)
async def root():
    """Root endpoint with API information"""
    return {
        "message": "IT Litigation System API",
        "version": "1.0.0",
        "docs": "/docs",
        "redoc": "/redoc",
        "status": "running"
    }

# Health check endpoint
@app.get("/health", response_model=dict)
async def health_check():
    """Health check endpoint"""
    db_healthy = await check_database_health()
    return {
        "status": "healthy" if db_healthy else "unhealthy",
        "database": "connected" if db_healthy else "disconnected",
        "timestamp": datetime.now(),
        "version": "1.0.0"
    }

# Document Processing API Endpoints
@app.get("/audit-logs/", response_model=List[AuditLogs])
async def list_audit_logs(
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(10, ge=1, le=100, description="Number of records to return"),
    filename: Optional[str] = Query(None, description="Filter by filename"),
    status_id: Optional[str] = Query(None, description="Filter by status ID"),
    pid: Optional[str] = Query(None, description="Filter by Process ID"),
    start_date: Optional[datetime] = Query(None, description="Filter by start date"),
    end_date: Optional[datetime] = Query(None, description="Filter by end date"),
):
    """Get audit logs records with optional filtering and pagination"""
    try:
        # Build filter
        filter_dict = {}
        if filename:
            filter_dict["filename"] = {"$regex": filename, "$options": "i"}
        if status_id:
            filter_dict["session.status.status_id"] = status_id
        if pid:
            filter_dict["session.PID"] = {"$regex": pid, "$options": "i"}
        if start_date or end_date:
            date_filter = {}
            if start_date:
                date_filter["$gte"] = start_date
            if end_date:
                date_filter["$lte"] = end_date
            filter_dict["created_at"] = date_filter
        
        documents = []
        async for document in audit_logs_collection.find(filter_dict).skip(skip).limit(limit).sort("created_at", -1):
            documents.append(audit_logs_helper(document))
        
        return documents
    except Exception as e:
        logger.error(f"Error fetching documents: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to fetch documents: {str(e)}")

# Error handlers
@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    """Custom HTTP exception handler"""
    return JSONResponse(
        status_code=exc.status_code,
        content=ErrorResponse(
            error=exc.detail,
            detail=f"HTTP {exc.status_code} error"
        ).dict()
    )

@app.exception_handler(Exception)
async def general_exception_handler(request, exc):
    """General exception handler"""
    logger.error(f"Unhandled exception: {exc}")
    return JSONResponse(
        status_code=500,
        content=ErrorResponse(
            error="Internal server error",
            detail="An unexpected error occurred"
        ).dict()
    )
