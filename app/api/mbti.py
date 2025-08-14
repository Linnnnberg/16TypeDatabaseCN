"""
MBTI API endpoints
Provides endpoints for MBTI type information and related functionality
"""

from fastapi import APIRouter, HTTPException
from typing import List, Dict

from app.data.mbti_types import (
    get_all_types_with_info,
    get_mbti_type_info,
    validate_mbti_type,
    get_all_types
)

router = APIRouter(prefix="/api/mbti", tags=["MBTI"])


@router.get("/types")
async def get_mbti_types():
    """
    Get all MBTI types with their information
    
    Returns:
        Dictionary containing all MBTI types with Chinese names, English names, and descriptions
    """
    try:
        types_data = get_all_types_with_info()
        return {
            "types": types_data,
            "total": len(types_data),
            "message": "MBTI types retrieved successfully"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving MBTI types: {str(e)}")


@router.get("/types/{type_code}")
async def get_mbti_type(type_code: str):
    """
    Get information for a specific MBTI type
    
    Args:
        type_code: The MBTI type code (e.g., "INTJ", "ENFP")
    
    Returns:
        Information for the specified MBTI type
    """
    if not validate_mbti_type(type_code):
        raise HTTPException(
            status_code=404, 
            detail=f"Invalid MBTI type: {type_code}. Must be one of {get_all_types()}"
        )
    
    try:
        type_info = get_mbti_type_info(type_code)
        if not type_info:
            raise HTTPException(status_code=404, detail=f"MBTI type not found: {type_code}")
        
        return {
            "code": type_code.upper(),
            "chinese_name": type_info["chinese"],
            "english_name": type_info["english"],
            "description": type_info["description"]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving MBTI type: {str(e)}")


@router.get("/types-list")
async def get_mbti_types_list():
    """
    Get a simple list of all MBTI type codes
    
    Returns:
        List of all MBTI type codes
    """
    try:
        return {
            "types": get_all_types(),
            "total": len(get_all_types()),
            "message": "MBTI type codes retrieved successfully"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving MBTI types list: {str(e)}")


@router.get("/validate/{type_code}")
async def validate_mbti_type_endpoint(type_code: str):
    """
    Validate if an MBTI type code is valid
    
    Args:
        type_code: The MBTI type code to validate
    
    Returns:
        Validation result
    """
    try:
        is_valid = validate_mbti_type(type_code)
        return {
            "type_code": type_code.upper(),
            "is_valid": is_valid,
            "message": f"MBTI type {type_code.upper()} is {'valid' if is_valid else 'invalid'}"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error validating MBTI type: {str(e)}")
