# Phase 1 Data Input Guide

## Overview
This guide explains how to use the Phase 1 data template system for adding celebrities and votes to your 16型花名册 application.

## What is Phase 1?
Phase 1 is the initial data seeding phase where you manually create celebrity data using templates and scripts, rather than building a full UI. This approach allows you to:
- Get data into the system quickly
- Focus on core functionality first
- Build admin tools based on actual usage patterns
- Maintain data quality through validation

## Quick Start

### 1. Edit the Template
Open `phase1_data_template.py` and modify the `CELEBRITIES_DATA` section:

```python
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
    # Add more celebrities here...
]
```

### 2. Run the Template Script
```bash
python phase1_data_template.py
```

This will:
- Validate your data
- Generate a properly formatted JSON file
- Save it to `data_uploads/pending/` folder
- Show you the next steps

### 3. Import the Data
The generated JSON file will be automatically placed in the pending folder. The upload service will process it and move it to the appropriate folder based on success/failure.

## Data Structure Requirements

### Required Fields
- **name**: Celebrity's name (max 100 characters)
- **mbti**: One of the 16 MBTI types (INTJ, INTP, ENTJ, etc.)
- **vote_reason**: Explanation for the MBTI type (max 1000 characters)

### Optional Fields
- **name_en**: English name
- **description**: Brief description
- **image_url**: URL to celebrity's image
- **tags**: Array of relevant tags

### MBTI Types Available
```
INTJ, INTP, ENTJ, ENTP,  # Analysts
INFJ, INFP, ENFJ, ENFP,  # Diplomats  
ISTJ, ISFJ, ESTJ, ESFJ,  # Sentinels
ISTP, ISFP, ESTP, ESFP   # Explorers
```

### Common Tags
- **Professions**: 演员, 歌手, 导演, 运动员, 音乐人
- **Regions**: 中国, 香港, 台湾, 美国, 英国
- **Characteristics**: 流量明星, 偶像, 实力派, 经典
- **Fields**: 电影, 音乐, 体育, 科技, 商业

## Validation Features

The template script automatically validates:
- Required fields are present
- MBTI types are valid
- Field lengths are within limits
- Data structure is correct

## File Naming Convention

Generated files follow this pattern:
```
celebrities_batch_YYYYMMDD_HHMMSS.json
```

Example: `celebrities_batch_20250812_152612.json`

## Workflow

1. **Edit Template** → Modify `phase1_data_template.py`
2. **Generate JSON** → Run the script
3. **Review Data** → Check the generated file
4. **Import** → File is automatically processed
5. **Verify** → Check `data_uploads/processed/` for success

## Tips for Good Data

### Vote Reasons
- Be specific about personality traits
- Reference observable behaviors
- Explain why the MBTI type fits
- Keep it factual and respectful

### Tags
- Use consistent terminology
- Include profession, region, and field
- Don't over-tag (3-5 tags per celebrity is good)
- Use existing tags when possible

### Names
- Use the most commonly known name
- Include English names for international celebrities
- Be consistent with naming conventions

## Troubleshooting

### Common Issues
1. **Validation Errors**: Check the error messages and fix the data
2. **Import Failures**: Check the processing logs in `data_uploads/`
3. **Duplicate Names**: The system prevents duplicate celebrity names

### Getting Help
- Check the processing logs in `data_uploads/processing_log.json`
- Review the generated JSON file for formatting issues
- Ensure all required fields are filled

## Next Steps

After Phase 1, you can:
1. Build a simple admin panel for basic CRUD operations
2. Create Wikipedia scraping tools for more data
3. Implement AI-powered data generation
4. Build a full content management system

## Files in This System

- `phase1_data_template.py` - Main template script
- `data_uploads/pending/` - Where new data goes
- `data_uploads/processed/` - Successfully imported data
- `data_uploads/failed/` - Failed imports
- `data_uploads/processing_log.json` - Import history

---

**Remember**: This is a development tool. In production, you'll want to build proper admin interfaces and data pipelines.
