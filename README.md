# IT Litigation System

A FastAPI-based document processing and audit logging system for IT litigation management.

## Features

- **Document Processing API**: Manage document processing records with status tracking
- **Audit Logging**: Track system activities and user actions
- **MongoDB Integration**: Async MongoDB operations with Motor driver
- **RESTful API**: Clean API endpoints with comprehensive filtering
- **Automatic Documentation**: Swagger UI and ReDoc integration
- **Health Monitoring**: Built-in health check endpoints

## API Structure

Based on collection.json structure with the following components:
- Document filename tracking
- Session management with Process IDs (PID)
- Status tracking (DR, E, P, C)
- Timestamp management

## Tech Stack

- **FastAPI**: Modern, fast web framework for building APIs
- **MongoDB**: NoSQL database for document storage
- **Motor**: Async MongoDB driver
- **Pydantic**: Data validation using Python type annotations
- **Uvicorn**: ASGI server implementation

## Installation

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd IT_Litigation
   ```

2. **Create virtual environment:**
   ```bash
   python -m venv venv
   venv\Scripts\activate  # Windows
   # or
   source venv/bin/activate  # Linux/Mac
   ```

3. **Install dependencies:**
   ```bash
   pip install fastapi uvicorn motor pymongo pydantic
   ```

4. **Start MongoDB:**
   - Install MongoDB locally or use MongoDB Atlas
   - Default connection: `mongodb://localhost:27017/IT_Litigation`

## Running the Application

1. **Start the FastAPI server:**
   ```bash
   uvicorn main:app --reload --host 127.0.0.1 --port 8000
   ```

2. **Access the API:**
   - API Base URL: `http://127.0.0.1:8000`
   - Swagger UI: `http://127.0.0.1:8000/docs`
   - ReDoc: `http://127.0.0.1:8000/redoc`

## API Endpoints

### Core Endpoints
- `GET /` - API information
- `GET /health` - Health check
- `GET /documents/` - Get document processing records

### Query Parameters for /documents/
- `skip` - Number of records to skip (pagination)
- `limit` - Number of records to return (max 100)
- `filename` - Filter by filename (partial match)
- `status_id` - Filter by status ID (DR, E, P, C)
- `pid` - Filter by Process ID
- `start_date` - Filter by start date
- `end_date` - Filter by end date

## Example Usage

### Get all documents
```bash
curl -X GET "http://127.0.0.1:8000/documents/"
```

### Filter by status
```bash
curl -X GET "http://127.0.0.1:8000/documents/?status_id=DR"
```

### Pagination
```bash
curl -X GET "http://127.0.0.1:8000/documents/?skip=0&limit=10"
```

## Project Structure

```
IT_Litigation/
├── main.py              # FastAPI application
├── models.py            # Helper functions for data processing
├── schemas.py           # Pydantic models for validation
├── database.py          # MongoDB connection and utilities
├── collection.json      # Sample data structure
├── venv/               # Virtual environment
└── README.md           # This file
```

## Data Model

Based on collection.json structure:

```json
{
  "_id": "ObjectId",
  "filename": "string",
  "session": {
    "PID": "UUID string",
    "status": {
      "status_id": "string (DR|E|P|C)",
      "message": "string"
    }
  },
  "created_at": "datetime",
  "updated_at": "datetime"
}
```

## Status Codes

- **DR**: Document Redacted
- **E**: Error during Processing
- **P**: Processing
- **C**: Completed

## Development

### Adding New Features
1. Update schemas in `schemas.py`
2. Add helper functions in `models.py`
3. Update database operations in `database.py`
4. Add API endpoints in `main.py`

### Testing
Use the provided Postman collection or curl commands to test the API endpoints.

## License

This project is licensed under the MIT License.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request
