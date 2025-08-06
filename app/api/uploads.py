#!/usr/bin/env python3
"""
API endpoints for JSON upload system
"""

from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, status
from sqlalchemy.orm import Session
from typing import Dict, Any
import json
from pathlib import Path
from datetime import datetime

from app.database.database import get_db
from app.services.json_upload_service import JSONUploadService
from app.core.security import get_current_admin_user
from app.database.models import User

router = APIRouter(prefix="/uploads", tags=["uploads"])


@router.post("/process-pending")
def process_pending_files(
    current_user: User = Depends(get_current_admin_user), db: Session = Depends(get_db)
):
    """
    Process all pending JSON files in the upload directory

    - **Admin only**: Requires admin authentication
    - **Automated**: Processes all .json files in data_uploads/pending/
    - **Validation**: Validates each file before processing
    - **Logging**: Creates detailed logs for success/failure
    """
    try:
        upload_service = JSONUploadService(db)
        results = upload_service.process_pending_files()

        return {
            "message": "Processing completed",
            "results": results,
            "timestamp": datetime.now().isoformat(),
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error processing files: {str(e)}",
        )


@router.get("/status")
def get_upload_status(
    current_user: User = Depends(get_current_admin_user), db: Session = Depends(get_db)
):
    """
    Get status of upload directories

    - **Admin only**: Requires admin authentication
    - **Returns**: Count and list of files in each directory
    """
    try:
        upload_service = JSONUploadService(db)
        status_info = upload_service.get_upload_status()

        return {"status": status_info, "timestamp": datetime.now().isoformat()}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error getting status: {str(e)}",
        )


@router.post("/upload-file")
def upload_json_file(
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_admin_user),
    db: Session = Depends(get_db),
):
    """
    Upload a JSON file for processing

    - **Admin only**: Requires admin authentication
    - **File**: Must be a valid JSON file
    - **Validation**: Validates file content before saving
    - **Processing**: File is saved to pending directory for processing
    """
    try:
        # Validate file type
        if not file.filename or not file.filename.endswith(".json"):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="File must be a JSON file",
            )

        # Read and validate JSON content
        content = file.file.read()
        try:
            json_data = json.loads(content.decode("utf-8"))
        except json.JSONDecodeError as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Invalid JSON format: {str(e)}",
            )

        # Validate data structure
        upload_service = JSONUploadService(db)

        # Create a temporary file for validation
        temp_path = Path("temp_validation.json")
        try:
            with open(temp_path, "w", encoding="utf-8") as f:
                json.dump(json_data, f, ensure_ascii=False, indent=2)

            validation_result = upload_service.validate_json_file(temp_path)

            if not validation_result["valid"]:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Data validation failed: {'; '.join(validation_result['errors'])}",
                )
        finally:
            # Clean up temp file
            if temp_path.exists():
                temp_path.unlink()

        # Save file to pending directory
        upload_service.pending_dir.mkdir(parents=True, exist_ok=True)
        file_path = upload_service.pending_dir / (file.filename or "unknown.json")

        with open(file_path, "wb") as f:
            f.write(content)

        return {
            "message": "File uploaded successfully",
            "filename": file.filename,
            "status": "pending",
            "timestamp": datetime.now().isoformat(),
        }

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error uploading file: {str(e)}",
        )


@router.post("/validate-file")
def validate_json_file(
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_admin_user),
    db: Session = Depends(get_db),
):
    """
    Validate a JSON file without processing it

    - **Admin only**: Requires admin authentication
    - **Validation**: Checks JSON format and data structure
    - **No Processing**: File is not saved or processed
    """
    try:
        # Read file content
        content = file.file.read()
        try:
            json_data = json.loads(content.decode("utf-8"))
        except json.JSONDecodeError as e:
            return {
                "valid": False,
                "errors": [f"Invalid JSON format: {str(e)}"],
                "filename": file.filename,
            }

        # Create temporary file for validation
        upload_service = JSONUploadService(db)
        temp_path = Path("temp_validation.json")

        try:
            with open(temp_path, "w", encoding="utf-8") as f:
                json.dump(json_data, f, ensure_ascii=False, indent=2)

            validation_result = upload_service.validate_json_file(temp_path)
            validation_result["filename"] = file.filename

            return validation_result

        finally:
            # Clean up temp file
            if temp_path.exists():
                temp_path.unlink()

    except Exception as e:
        return {
            "valid": False,
            "errors": [f"Validation error: {str(e)}"],
            "filename": file.filename,
        }


@router.get("/schema")
def get_json_schema():
    """
    Get the JSON schema for upload files

    - **Public**: No authentication required
    - **Schema**: Returns the expected JSON structure
    """
    return {
        "schema": {
            "celebrities": [
                {
                    "name": "名人姓名 (required)",
                    "name_en": "English Name (optional)",
                    "description": "简短描述 (optional)",
                    "image_url": "https://example.com/image.jpg (optional)",
                    "mbti": "INTJ (required - one of 16 MBTI types)",
                    "vote_reason": "MBTI类型理由 (required)",
                    "tags": "[\"标签1\", \"标签2\"] (optional)",
                }
            ],
            "metadata": {
                "source": "数据来源 (optional)",
                "version": "1.0 (optional)",
                "upload_date": "2024-01-01 (optional)",
            },
        },
        "mbti_types": [
            "INTJ",
            "INTP",
            "ENTJ",
            "ENTP",
            "INFJ",
            "INFP",
            "ENFJ",
            "ENFP",
            "ISTJ",
            "ISFJ",
            "ESTJ",
            "ESFJ",
            "ISTP",
            "ISFP",
            "ESTP",
            "ESFP",
        ],
        "example": {
            "celebrities": [
                {
                    "name": "周杰伦",
                    "name_en": "Jay Chou",
                    "description": "台湾著名歌手、音乐人、演员、导演",
                    "image_url": "",
                    "mbti": "INTP",
                    "vote_reason": "周杰伦表现出INTP的特点：内向、理性、创新思维，在音乐创作中展现独特的逻辑性和创造力。",
                    "tags": ["歌手", "音乐人", "演员", "导演", "台湾"],
                }
            ],
            "metadata": {
                "source": "MBTI分析社区",
                "version": "1.0",
                "upload_date": "2024-01-01",
            },
        },
    }
