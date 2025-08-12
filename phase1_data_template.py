#!/usr/bin/env python3
"""
Phase 1 Data Template Script for 16型花名册
Easy way to create properly formatted JSON data for bulk imports

Usage:
1. Modify the data below
2. Run this script to generate JSON files
3. Place generated files in data_uploads/pending/ folder
4. Use the upload service to import the data
"""

import json
import os
from datetime import datetime
from pathlib import Path

# ============================================================================
# DATA TEMPLATE - MODIFY THIS SECTION
# ============================================================================

# Template for adding new celebrities with votes
CELEBRITIES_DATA = [
    {
        "name": "名人姓名",
        "name_en": "English Name (optional)",
        "description": "简短描述 (optional)",
        "image_url": "https://example.com/image.jpg",  # optional
        "mbti": "INTJ",  # 16种MBTI类型之一
        "vote_reason": "为什么认为这个名人是这个MBTI类型的理由",
        "tags": ["标签1", "标签2", "标签3"],  # 相关标签
    },
    # 复制上面的格式添加更多名人
    {
        "name": "周杰伦",
        "name_en": "Jay Chou",
        "description": "台湾著名歌手、音乐人、演员、导演",
        "image_url": "",
        "mbti": "INTP",
        "vote_reason": "周杰伦表现出INTP的特点：内向、理性、创新思维，在音乐创作中展现独特的逻辑性和创造力。",
        "tags": ["歌手", "音乐人", "演员", "导演", "台湾"],
    },
    {
        "name": "刘翔",
        "name_en": "Liu Xiang",
        "description": "中国著名田径运动员，110米栏奥运冠军",
        "image_url": "",
        "mbti": "ESTJ",
        "vote_reason": "作为田径跨栏英雄，执行力强、目标导向明显，常被粉丝推测为 ESTJ 类型",
        "tags": ["运动员", "田径", "奥运冠军", "中国"],
    }
]

# ============================================================================
# CONFIGURATION
# ============================================================================

# Output directory
OUTPUT_DIR = Path("data_uploads/pending")

# File naming
FILE_PREFIX = "celebrities_batch"
FILE_SUFFIX = ".json"

# Metadata for the upload
METADATA = {
    "source": "phase1_manual_input",
    "version": "1.0",
    "upload_date": datetime.now().isoformat(),
    "description": "Phase 1 celebrity data for initial system seeding"
}

# ============================================================================
# VALIDATION
# ============================================================================

# Available MBTI types
MBTI_TYPES = [
    "INTJ", "INTP", "ENTJ", "ENTP",
    "INFJ", "INFP", "ENFJ", "ENFP",
    "ISTJ", "ISFJ", "ESTJ", "ESFJ",
    "ISTP", "ISFP", "ESTP", "ESFP"
]

# Common tags for reference
COMMON_TAGS = [
    # 职业
    "演员", "歌手", "导演", "制片人", "音乐人", "舞者", "编剧", "主持人",
    "运动员", "教练", "记者", "作家", "画家", "摄影师", "设计师",
    # 地区
    "中国", "香港", "台湾", "美国", "英国", "日本", "韩国", "欧洲",
    # 特点
    "流量明星", "偶像", "实力派", "国际化", "新生代", "经典", "传奇",
    # 领域
    "电影", "电视剧", "音乐", "综艺", "体育", "科技", "商业", "艺术"
]

def validate_celebrity_data(celeb):
    """Validate celebrity data structure and content"""
    errors = []
    
    # Required fields
    if not celeb.get("name"):
        errors.append("Missing required field: name")
    if not celeb.get("mbti"):
        errors.append("Missing required field: mbti")
    if not celeb.get("vote_reason"):
        errors.append("Missing required field: vote_reason")
    
    # MBTI type validation
    if celeb.get("mbti") and celeb["mbti"] not in MBTI_TYPES:
        errors.append(f"Invalid MBTI type: {celeb['mbti']}. Must be one of {MBTI_TYPES}")
    
    # Name length validation
    if celeb.get("name") and len(celeb["name"]) > 100:
        errors.append("Name too long (max 100 characters)")
    
    # Reason length validation
    if celeb.get("vote_reason") and len(celeb["vote_reason"]) > 1000:
        errors.append("Vote reason too long (max 1000 characters)")
    
    return errors

def validate_all_data():
    """Validate all celebrity data"""
    all_errors = []
    
    for i, celeb in enumerate(CELEBRITIES_DATA):
        errors = validate_celebrity_data(celeb)
        if errors:
            all_errors.append(f"Celebrity {i+1} ({celeb.get('name', 'Unknown')}): {', '.join(errors)}")
    
    return all_errors

def generate_upload_json():
    """Generate the properly formatted JSON for upload service"""
    return {
        "celebrities": CELEBRITIES_DATA,
        "metadata": METADATA
    }

def save_json_file(data, filename):
    """Save JSON data to file"""
    # Ensure output directory exists
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    
    filepath = OUTPUT_DIR / filename
    
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    return filepath

def main():
    """Main function to generate and save data files"""
    print("=== Phase 1 Data Template Script ===")
    print(f"Processing {len(CELEBRITIES_DATA)} celebrities...")
    
    # Validate data
    print("\nValidating data...")
    validation_errors = validate_all_data()
    
    if validation_errors:
        print("❌ Validation errors found:")
        for error in validation_errors:
            print(f"  - {error}")
        print("\nPlease fix the errors before proceeding.")
        return False
    
    print("✅ All data validation passed!")
    
    # Generate upload JSON
    upload_data = generate_upload_json()
    
    # Generate filename with timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{FILE_PREFIX}_{timestamp}{FILE_SUFFIX}"
    
    # Save file
    try:
        filepath = save_json_file(upload_data, filename)
        print(f"\n✅ JSON file generated successfully!")
        print(f"📁 File: {filepath}")
        print(f"📊 Celebrities: {len(CELEBRITIES_DATA)}")
        
        # Show next steps
        print("\n📋 Next steps:")
        print("1. Review the generated JSON file")
        print("2. Place it in data_uploads/pending/ folder")
        print("3. Use the upload service to import the data")
        print("4. Check data_uploads/processed/ for success confirmation")
        
        return True
        
    except Exception as e:
        print(f"❌ Error saving file: {e}")
        return False

def show_data_summary():
    """Show summary of current data"""
    print("\n=== Current Data Summary ===")
    print(f"Total celebrities: {len(CELEBRITIES_DATA)}")
    
    # Count by MBTI type
    mbti_counts = {}
    for celeb in CELEBRITIES_DATA:
        mbti = celeb.get("mbti", "Unknown")
        mbti_counts[mbti] = mbti_counts.get(mbti, 0) + 1
    
    print("\nMBTI Type Distribution:")
    for mbti_type in sorted(MBTI_TYPES):
        count = mbti_counts.get(mbti_type, 0)
        print(f"  {mbti_type}: {count}")
    
    # Show all tags used
    all_tags = set()
    for celeb in CELEBRITIES_DATA:
        all_tags.update(celeb.get("tags", []))
    
    print(f"\nTags used: {', '.join(sorted(all_tags))}")

if __name__ == "__main__":
    # Show data summary first
    show_data_summary()
    
    # Generate files
    success = main()
    
    if success:
        print("\n🎉 Phase 1 data template completed successfully!")
    else:
        print("\n💥 Phase 1 data template failed. Please check the errors above.")
