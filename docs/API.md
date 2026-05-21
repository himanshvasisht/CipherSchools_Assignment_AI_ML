# API Specification

The backend runs a FastAPI REST server. The interactive API documentation is available via Swagger at `{API_BASE_URL}/docs`.

## Endpoint Summary

### 1. Root Status
- **URL**: `/`
- **Method**: `GET`
- **Description**: Verifies the status of the server.
- **Response**:
  ```json
  {
      "status": "running"
  }
  ```

### 2. Run Review
- **URL**: `/review`
- **Method**: `POST`
- **Headers**: `Content-Type: application/json`
- **Request Body**:
  ```json
  {
      "repo_url": "https://github.com/owner/repo"
  }
  ```
- **Response**:
  ```json
  {
      "success": true,
      "repo": "https://github.com/owner/repo",
      "files_scanned": 12,
      "chunks": 43,
      "dependency_nodes": 8,
      "reviews": [
          {
              "name": "process_data",
              "type": "function",
              "file": "temp_repos/test_repo/src/utils.py",
              "risk_score": 35,
              "confidence": 78,
              "verify": false,
              "security": [],
              "pylint": "pylint findings details...",
              "code_preview": "def process_data(data):\n    pass",
              "llm_review": "### Quality Agent findings:\n...",
              "repair_suggestions": "🔧 Repair suggestions..."
          }
      ],
      "runtime_sec": 42.12
  }
  ```
