#!/usr/bin/env python3
"""
JSON Upload Service for automated celebrity data import
"""

import json

import shutil
from datetime import datetime
from typing import List, Dict, Any, Optional
from pathlib import Path
from pydantic import BaseModel, ValidationError
from sqlalchemy.orm import Session

from app.database.models import (
    Celebrity,
    Tag,
    CelebrityTag,
    Vote,
    User,
    UserRole,
    MBTIType,
)
from app.services.celebrity_service import CelebrityService
from app.services.vote_service import VoteService
import uuid


class CelebrityData(BaseModel):
    """Pydantic model for celebrity data validation"""

    name: str
    name_en: Optional[str] = None
    description: Optional[str] = None
    image_url: Optional[str] = None
    mbti: str
    vote_reason: str
    tags: List[str] = []


class UploadMetadata(BaseModel):
    """Pydantic model for upload metadata"""

    source: Optional[str] = None
    version: str = "1.0"
    upload_date: Optional[str] = None


class UploadData(BaseModel):
    """Pydantic model for complete upload data"""

    celebrities: List[CelebrityData]
    metadata: Optional[UploadMetadata] = None


class JSONUploadService:
    """Service for handling JSON file uploads and data import"""

    def __init__(self, db: Session):
        self.db = db
        self.celebrity_service = CelebrityService(db)
        self.vote_service = VoteService(db)

        # Upload directories
        self.base_dir = Path("data_uploads")
        self.pending_dir = self.base_dir / "pending"
        self.processed_dir = self.base_dir / "processed"
        self.failed_dir = self.base_dir / "failed"

        # Ensure directories exist
        self.pending_dir.mkdir(parents=True, exist_ok=True)
        self.processed_dir.mkdir(parents=True, exist_ok=True)
        self.failed_dir.mkdir(parents=True, exist_ok=True)

    def validate_json_file(self, file_path: Path) -> Dict[str, Any]:
        """Validate JSON file structure and content"""
        try:
            # Read and parse JSON
            with open(file_path, "r", encoding="utf-8") as f:
                data = json.load(f)

            # Validate with Pydantic
            upload_data = UploadData(**data)

            # Additional validation
            validation_errors = []

            # Check MBTI types
            valid_mbti_types = [mbti.value for mbti in MBTIType]
            for i, celeb in enumerate(upload_data.celebrities):
                if celeb.mbti not in valid_mbti_types:
                    validation_errors.append(
                        f"Celebrity {i+1} ({celeb.name}): "
                        f"Invalid MBTI type '{celeb.mbti}'"
                    )

                # Check for duplicate names
                existing_celebrity = self.celebrity_service.get_celebrity_by_name(
                    celeb.name
                )
                if existing_celebrity:
                    validation_errors.append(
                        f"Celebrity {i+1} ({celeb.name}): Already exists in database"
                    )

            if validation_errors:
                return {"valid": False, "errors": validation_errors, "data": None}

            return {"valid": True, "errors": [], "data": upload_data}

        except json.JSONDecodeError as e:
            return {
                "valid": False,
                "errors": [f"Invalid JSON format: {str(e)}"],
                "data": None,
            }
        except ValidationError as e:
            return {
                "valid": False,
                "errors": [f"Data validation error: {str(e)}"],
                "data": None,
            }
        except Exception as e:
            return {
                "valid": False,
                "errors": [f"Unexpected error: {str(e)}"],
                "data": None,
            }

    def process_upload_data(self, upload_data: UploadData) -> Dict[str, Any]:
        """Process validated upload data and import to database"""
        try:
            # Get system user for votes
            system_user = (
                self.db.query(User).filter(User.role == UserRole.SYSTEM).first()
            )
            if not system_user:
                return {
                    "success": False,
                    "errors": [
                        "System user not found. Please run create_admin.py first."
                    ],
                    "imported_count": 0,
                }

            # Track existing tags
            existing_tags = {tag.name: tag for tag in self.db.query(Tag).all()}

            imported_count = 0
            errors = []

            for celeb_data in upload_data.celebrities:
                try:
                    # Create celebrity
                    celebrity = Celebrity(
                        id=str(uuid.uuid4()),
                        name=celeb_data.name,
                        name_en=celeb_data.name_en,
                        description=celeb_data.description,
                        image_url=celeb_data.image_url,
                        created_at=datetime.utcnow(),
                        updated_at=datetime.utcnow(),
                    )
                    self.db.add(celebrity)
                    self.db.flush()  # Get the ID

                    # Create vote
                    vote = Vote(
                        id=str(uuid.uuid4()),
                        user_id=system_user.id,
                        celebrity_id=celebrity.id,
                        mbti_type=MBTIType(celeb_data.mbti),
                        reason=celeb_data.vote_reason,
                        created_at=datetime.utcnow(),
                    )
                    self.db.add(vote)

                    # Handle tags
                    for tag_name in celeb_data.tags:
                        if tag_name not in existing_tags:
                            tag = Tag(
                                id=str(uuid.uuid4()),
                                name=tag_name,
                                created_at=datetime.utcnow(),
                            )
                            self.db.add(tag)
                            existing_tags[tag_name] = tag

                        # Create celebrity-tag relationship
                        celebrity_tag = CelebrityTag(
                            celebrity_id=celebrity.id, tag_id=existing_tags[tag_name].id
                        )
                        self.db.add(celebrity_tag)

                    imported_count += 1

                except Exception as e:
                    errors.append(f"Error importing {celeb_data.name}: {str(e)}")

            # Commit all changes
            if errors:
                self.db.rollback()
                return {"success": False, "errors": errors, "imported_count": 0}
            else:
                self.db.commit()
                return {"success": True, "errors": [], "imported_count": imported_count}

        except Exception as e:
            self.db.rollback()
            return {
                "success": False,
                "errors": [f"Database error: {str(e)}"],
                "imported_count": 0,
            }

    def process_pending_files(self) -> Dict[str, Any]:
        """Process all pending JSON files in the upload directory"""
        results: Dict[str, Any] = {
            "processed_files": 0,
            "successful_imports": 0,
            "failed_imports": 0,
            "errors": [],
        }

        # Get all JSON files in pending directory
        json_files = list(self.pending_dir.glob("*.json"))

        for file_path in json_files:
            try:
                # Validate file
                validation_result = self.validate_json_file(file_path)

                if not validation_result["valid"]:
                    # Move to failed directory
                    failed_path = self.failed_dir / file_path.name
                    shutil.move(str(file_path), str(failed_path))

                    # Create error log
                    error_log_path = self.failed_dir / f"{file_path.stem}_errors.txt"
                    with open(error_log_path, "w", encoding="utf-8") as f:
                        f.write(f"File: {file_path.name}\n")
                        f.write(f"Timestamp: {datetime.now().isoformat()}\n")
                        f.write("Validation Errors:\n")
                        for error in validation_result["errors"]:
                            f.write(f"- {error}\n")

                    results["failed_imports"] += 1
                    results["errors"].append(f"{file_path.name}: Validation failed")
                    continue

                # Process data
                process_result = self.process_upload_data(validation_result["data"])

                if process_result["success"]:
                    # Move to processed directory
                    processed_path = self.processed_dir / file_path.name
                    shutil.move(str(file_path), str(processed_path))

                    # Create success log
                    success_log_path = (
                        self.processed_dir / f"{file_path.stem}_success.txt"
                    )
                    with open(success_log_path, "w", encoding="utf-8") as f:
                        f.write(f"File: {file_path.name}\n")
                        f.write(f"Timestamp: {datetime.now().isoformat()}\n")
                        f.write(
                            f"Imported: {process_result['imported_count']} "
                            f"celebrities\n"
                        )

                    results["successful_imports"] += 1
                else:
                    # Move to failed directory
                    failed_path = self.failed_dir / file_path.name
                    shutil.move(str(file_path), str(failed_path))

                    # Create error log
                    error_log_path = self.failed_dir / f"{file_path.stem}_errors.txt"
                    with open(error_log_path, "w", encoding="utf-8") as f:
                        f.write(f"File: {file_path.name}\n")
                        f.write(f"Timestamp: {datetime.now().isoformat()}\n")
                        f.write("Processing Errors:\n")
                        for error in process_result["errors"]:
                            f.write(f"- {error}\n")

                    results["failed_imports"] += 1
                    results["errors"].extend(
                        [
                            f"{file_path.name}: {error}"
                            for error in process_result["errors"]
                        ]
                    )

                results["processed_files"] += 1

            except Exception as e:
                # Move to failed directory
                failed_path = self.failed_dir / file_path.name
                shutil.move(str(file_path), str(failed_path))

                results["failed_imports"] += 1
                results["errors"].append(
                    f"{file_path.name}: Unexpected error - {str(e)}"
                )

        return results

    def get_upload_status(self) -> Dict[str, Any]:
        """Get status of upload directories"""
        return {
            "pending_files": len(list(self.pending_dir.glob("*.json"))),
            "processed_files": len(list(self.processed_dir.glob("*.json"))),
            "failed_files": len(list(self.failed_dir.glob("*.json"))),
            "pending_list": [f.name for f in self.pending_dir.glob("*.json")],
            "processed_list": [f.name for f in self.processed_dir.glob("*.json")],
            "failed_list": [f.name for f in self.failed_dir.glob("*.json")],
        }
