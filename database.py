from motor.motor_asyncio import AsyncIOMotorClient
from datetime import datetime
import os

# MongoDB connection from environment variable
MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/IT_Litigation")
client = AsyncIOMotorClient(MONGO_URI)
database = client.IT_Litigation

# Collections
audit_logs_collection = database["audit_logs"]

# Database utility functions
async def get_database():
    """Get database instance"""
    return database

async def get_collection(collection_name: str):
    """Get a specific collection"""
    return database[collection_name]

# Index creation for better performance
async def create_indexes():
    """Create indexes for better query performance"""
    try:
        # Audit logs indexes
        await audit_logs_collection.create_index("filename")
        await audit_logs_collection.create_index("session.PID")
        await audit_logs_collection.create_index("session.status.status_id")
        await audit_logs_collection.create_index("created_at")
        await audit_logs_collection.create_index("updated_at")
        
        print("Database indexes created successfully")
    except Exception as e:
        print(f"Error creating indexes: {e}")

# Health check function
async def check_database_health():
    """Check database connection health"""
    try:
        await database.command("ping")
        return True
    except Exception as e:
        print(f"Database health check failed: {e}")
        return False

# Collections
audit_logs_collection = database["audit_logs"]

# Database utility functions
async def get_database():
    """Get database instance"""
    return database

async def get_collection(collection_name: str):
    """Get a specific collection"""
    return database[collection_name]

# Index creation for better performance
async def create_indexes():
    """Create indexes for better query performance"""
    try:
        # Audit logs indexes
        await audit_logs_collection.create_index("filename")
        await audit_logs_collection.create_index("session.PID")
        await audit_logs_collection.create_index("session.status.status_id")
        await audit_logs_collection.create_index("created_at")
        await audit_logs_collection.create_index("updated_at")
        
        print("Database indexes created successfully")
    except Exception as e:
        print(f"Error creating indexes: {e}")

# Health check function
async def check_database_health():
    """Check database connection health"""
    try:
        await database.command("ping")
        return True
    except Exception as e:
        print(f"Database health check failed: {e}")
        return False