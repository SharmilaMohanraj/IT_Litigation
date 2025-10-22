from bson import ObjectId
from datetime import datetime
from typing import Dict, Any

def audit_logs_status_helper(status_data: Dict[str, Any]) -> dict:
    """Helper function for audit logs status data"""
    return {
        "status_id": status_data["status_id"],
        "message": status_data["message"]
    }

def audit_logs_session_helper(session_data: Dict[str, Any]) -> dict:
    """Helper function for audit logs session data"""
    return {
        "PID": session_data["PID"],
        "status": audit_logs_status_helper(session_data["status"])
    }

def audit_logs_helper(document) -> dict:
    """Helper function for audit logs data based on collection.json structure"""
    return {
        "id": str(document["_id"]),
        "filename": document["filename"],
        "session": audit_logs_session_helper(document["session"]),
        "created_at": document.get("created_at", datetime.now()),
        "updated_at": document.get("updated_at", datetime.now())
    }
