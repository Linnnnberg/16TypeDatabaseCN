#!/usr/bin/env python3
"""
Fix and Process Pending Data Files - TECH-005

This script fixes format issues in pending data files and processes them
for import into the database.
"""

import json
import shutil
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any, Optional
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Import database models and services
from app.database.database import engine
from app.database.models import Celebrity, Tag, CelebrityTag, Vote, User, UserRole, MBTIType
from app.services.json_upload_service import JSONUploadService
from app.services.celebrity_service import CelebrityService
from app.services.vote_service import VoteService
import uuid


class PendingDataProcessor:
    """Process and fix pending data files"""
    
    def __init__(self):
        self.base_dir = Path("data_uploads")
        self.pending_dir = self.base_dir / "pending"
        self.processed_dir = self.base_dir / "processed"
        self.failed_dir = self.base_dir / "failed"
        self.fixed_dir = self.base_dir / "fixed"
        
        # Ensure directories exist
        for dir_path in [self.pending_dir, self.processed_dir, self.failed_dir, self.fixed_dir]:
            dir_path.mkdir(parents=True, exist_ok=True)
        
        # Database setup
        SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
        self.db = SessionLocal()
        self.upload_service = JSONUploadService(self.db)
        self.celebrity_service = CelebrityService(self.db)
        self.vote_service = VoteService(self.db)
    
    def fix_celebrities_batch_sports(self) -> Dict[str, Any]:
        """Fix the format of celebrities_batch_sports.json"""
        file_path = self.pending_dir / "celebrities_batch_sports.json"
        
        if not file_path.exists():
            return {"success": False, "error": "File not found"}
        
        try:
            # Read the array format
            with open(file_path, 'r', encoding='utf-8') as f:
                celebrities_array = json.load(f)
            
            # Convert to proper format
            fixed_data = {
                "celebrities": celebrities_array,
                "metadata": {
                    "source": "Sports Celebrities Batch",
                    "version": "1.0",
                    "upload_date": datetime.now().strftime("%Y-%m-%d"),
                    "fixed": True
                }
            }
            
            # Save fixed version
            fixed_path = self.fixed_dir / "celebrities_batch_sports_fixed.json"
            with open(fixed_path, 'w', encoding='utf-8') as f:
                json.dump(fixed_data, f, ensure_ascii=False, indent=2)
            
            # Move original to failed
            failed_path = self.failed_dir / "celebrities_batch_sports_original.json"
            shutil.move(str(file_path), str(failed_path))
            
            return {
                "success": True,
                "message": "Fixed celebrities_batch_sports.json format",
                "fixed_file": str(fixed_path),
                "original_moved_to": str(failed_path)
            }
            
        except Exception as e:
            return {"success": False, "error": f"Error fixing file: {str(e)}"}
    
    def fix_votes_batch_sports(self) -> Dict[str, Any]:
        """Fix the format of votes_batch_sports.json and merge with celebrities"""
        votes_file = self.pending_dir / "votes_batch_sports.json"
        celebrities_file = self.fixed_dir / "celebrities_batch_sports_fixed.json"
        
        if not votes_file.exists():
            return {"success": False, "error": "Votes file not found"}
        
        if not celebrities_file.exists():
            return {"success": False, "error": "Fixed celebrities file not found"}
        
        try:
            # Read votes array
            with open(votes_file, 'r', encoding='utf-8') as f:
                votes_array = json.load(f)
            
            # Read fixed celebrities
            with open(celebrities_file, 'r', encoding='utf-8') as f:
                celebrities_data = json.load(f)
            
            # Create a mapping of names to votes
            votes_map = {vote["name"]: vote for vote in votes_array}
            
            # Merge votes into celebrities data
            for celebrity in celebrities_data["celebrities"]:
                if celebrity["name"] in votes_map:
                    vote_data = votes_map[celebrity["name"]]
                    celebrity["mbti"] = vote_data["mbti"]
                    celebrity["vote_reason"] = vote_data["comment"]
                else:
                    # Add default values for celebrities without votes
                    celebrity["mbti"] = "UNKNOWN"
                    celebrity["vote_reason"] = "No vote data available"
            
            # Save merged data
            merged_path = self.fixed_dir / "celebrities_batch_sports_merged.json"
            with open(merged_path, 'w', encoding='utf-8') as f:
                json.dump(celebrities_data, f, ensure_ascii=False, indent=2)
            
            # Move original votes file to failed
            failed_path = self.failed_dir / "votes_batch_sports_original.json"
            shutil.move(str(votes_file), str(failed_path))
            
            return {
                "success": True,
                "message": "Merged votes with celebrities data",
                "merged_file": str(merged_path),
                "votes_moved_to": str(failed_path)
            }
            
        except Exception as e:
            return {"success": False, "error": f"Error merging votes: {str(e)}"}
    
    def handle_duplicate_celebrities(self) -> Dict[str, Any]:
        """Handle duplicate celebrities in sample_celebrities.json"""
        file_path = self.pending_dir / "sample_celebrities.json"
        
        if not file_path.exists():
            return {"success": False, "error": "Sample celebrities file not found"}
        
        try:
            # Read the file
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # Check for duplicates
            existing_celebrities = []
            new_celebrities = []
            
            for celebrity in data["celebrities"]:
                existing = self.celebrity_service.get_celebrity_by_name(celebrity["name"])
                if existing:
                    existing_celebrities.append(celebrity["name"])
                else:
                    new_celebrities.append(celebrity)
            
            if not new_celebrities:
                # All celebrities already exist
                failed_path = self.failed_dir / "sample_celebrities_all_duplicates.json"
                shutil.move(str(file_path), str(failed_path))
                
                return {
                    "success": True,
                    "message": "All celebrities already exist in database",
                    "existing_count": len(existing_celebrities),
                    "new_count": 0,
                    "file_moved_to": str(failed_path)
                }
            
            # Create new file with only new celebrities
            if len(new_celebrities) < len(data["celebrities"]):
                new_data = {
                    "celebrities": new_celebrities,
                    "metadata": {
                        **data["metadata"],
                        "filtered": True,
                        "original_count": len(data["celebrities"]),
                        "new_count": len(new_celebrities),
                        "duplicates_removed": existing_celebrities
                    }
                }
                
                # Save filtered data
                filtered_path = self.fixed_dir / "sample_celebrities_filtered.json"
                with open(filtered_path, 'w', encoding='utf-8') as f:
                    json.dump(new_data, f, ensure_ascii=False, indent=2)
                
                # Move original to failed
                failed_path = self.failed_dir / "sample_celebrities_original.json"
                shutil.move(str(file_path), str(failed_path))
                
                return {
                    "success": True,
                    "message": f"Filtered {len(new_celebrities)} new celebrities",
                    "existing_count": len(existing_celebrities),
                    "new_count": len(new_celebrities),
                    "filtered_file": str(filtered_path),
                    "original_moved_to": str(failed_path)
                }
            
            return {
                "success": True,
                "message": "No duplicates found, file is ready for processing",
                "existing_count": len(existing_celebrities),
                "new_count": len(new_celebrities)
            }
            
        except Exception as e:
            return {"success": False, "error": f"Error handling duplicates: {str(e)}"}
    
    def process_fixed_files(self) -> Dict[str, Any]:
        """Process all fixed files in the fixed directory"""
        results = {
            "processed_files": 0,
            "successful_imports": 0,
            "failed_imports": 0,
            "errors": []
        }
        
        # Get all JSON files in fixed directory
        json_files = list(self.fixed_dir.glob("*.json"))
        
        for file_path in json_files:
            try:
                # Validate file
                validation_result = self.upload_service.validate_json_file(file_path)
                
                if not validation_result["valid"]:
                    # Move to failed directory
                    failed_path = self.failed_dir / file_path.name
                    shutil.move(str(file_path), str(failed_path))
                    
                    results["failed_imports"] += 1
                    results["errors"].extend([
                        f"{file_path.name}: {error}"
                        for error in validation_result["errors"]
                    ])
                    continue
                
                # Process the data
                process_result = self.upload_service.process_upload_data(validation_result["data"])
                
                if process_result["success"]:
                    # Move to processed directory
                    processed_path = self.processed_dir / file_path.name
                    shutil.move(str(file_path), str(processed_path))
                    
                    results["successful_imports"] += 1
                else:
                    # Move to failed directory
                    failed_path = self.failed_dir / file_path.name
                    shutil.move(str(file_path), str(failed_path))
                    
                    results["failed_imports"] += 1
                    results["errors"].extend([
                        f"{file_path.name}: {error}"
                        for error in process_result["errors"]
                    ])
                
                results["processed_files"] += 1
                
            except Exception as e:
                # Move to failed directory
                failed_path = self.failed_dir / file_path.name
                shutil.move(str(file_path), str(failed_path))
                
                results["failed_imports"] += 1
                results["errors"].append(f"{file_path.name}: Unexpected error - {str(e)}")
        
        return results
    
    def run_full_processing(self) -> Dict[str, Any]:
        """Run the complete processing pipeline"""
        print("=== Fix and Process Pending Data Files ===")
        print(f"Timestamp: {datetime.now().isoformat()}")
        print()
        
        results = {
            "fix_results": {},
            "processing_results": {},
            "summary": {}
        }
        
        # Step 1: Fix celebrities_batch_sports.json
        print("1. Fixing celebrities_batch_sports.json...")
        fix_result = self.fix_celebrities_batch_sports()
        results["fix_results"]["celebrities_batch_sports"] = fix_result
        print(f"   Result: {'SUCCESS' if fix_result['success'] else 'FAILED'}")
        if not fix_result['success']:
            print(f"   Error: {fix_result['error']}")
        
        # Step 2: Fix votes_batch_sports.json
        print("2. Fixing votes_batch_sports.json...")
        votes_result = self.fix_votes_batch_sports()
        results["fix_results"]["votes_batch_sports"] = votes_result
        print(f"   Result: {'SUCCESS' if votes_result['success'] else 'FAILED'}")
        if not votes_result['success']:
            print(f"   Error: {votes_result['error']}")
        
        # Step 3: Handle duplicates in sample_celebrities.json
        print("3. Handling duplicates in sample_celebrities.json...")
        duplicates_result = self.handle_duplicate_celebrities()
        results["fix_results"]["sample_celebrities"] = duplicates_result
        print(f"   Result: {'SUCCESS' if duplicates_result['success'] else 'FAILED'}")
        if not duplicates_result['success']:
            print(f"   Error: {duplicates_result['error']}")
        
        # Step 4: Process all fixed files
        print("4. Processing fixed files...")
        processing_result = self.process_fixed_files()
        results["processing_results"] = processing_result
        print(f"   Processed: {processing_result['processed_files']} files")
        print(f"   Successful: {processing_result['successful_imports']} imports")
        print(f"   Failed: {processing_result['failed_imports']} imports")
        
        # Summary
        results["summary"] = {
            "total_fixes": len([r for r in results["fix_results"].values() if r.get("success")]),
            "total_processed": processing_result["processed_files"],
            "total_successful": processing_result["successful_imports"],
            "total_failed": processing_result["failed_imports"],
            "timestamp": datetime.now().isoformat()
        }
        
        print()
        print("=== Processing Complete ===")
        print(f"Fixes applied: {results['summary']['total_fixes']}")
        print(f"Files processed: {results['summary']['total_processed']}")
        print(f"Successful imports: {results['summary']['total_successful']}")
        print(f"Failed imports: {results['summary']['total_failed']}")
        
        if processing_result["errors"]:
            print("\nErrors:")
            for error in processing_result["errors"]:
                print(f"  - {error}")
        
        return results
    
    def cleanup(self):
        """Clean up database connection"""
        self.db.close()


def main():
    """Main function to run the data processing"""
    processor = PendingDataProcessor()
    
    try:
        results = processor.run_full_processing()
        
        # Save results to log file
        log_path = Path("data_uploads/processing_log.json")
        with open(log_path, 'w', encoding='utf-8') as f:
            json.dump(results, f, ensure_ascii=False, indent=2)
        
        print(f"\nDetailed results saved to: {log_path}")
        
    except Exception as e:
        print(f"Error during processing: {str(e)}")
        return 1
    finally:
        processor.cleanup()
    
    return 0


if __name__ == "__main__":
    exit(main())
