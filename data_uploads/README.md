# JSON Upload System

This directory contains the automated JSON upload system for importing celebrity data into the 16型花名册 database.

## Directory Structure

```
data_uploads/
├── pending/          # Place JSON files here for processing
├── processed/        # Successfully processed files
├── failed/          # Files that failed validation/processing
├── sample_celebrities.json  # Example file format
└── README.md        # This file
```

## How to Use

### Method 1: File System Upload (Recommended)

1. **Prepare your JSON file** using the format below
2. **Place the file** in the `pending/` directory
3. **Trigger processing** via API endpoint: `POST /uploads/process-pending`
4. **Check results** in `processed/` or `failed/` directories

### Method 2: API Upload

1. **Use the API endpoint**: `POST /uploads/upload-file`
2. **Upload your JSON file** via the API
3. **File will be validated** and placed in `pending/` if valid
4. **Process manually** or wait for automated processing

## JSON File Format

### Required Structure

```json
{
  "celebrities": [
    {
      "name": "名人姓名",
      "name_en": "English Name",
      "description": "简短描述",
      "image_url": "https://example.com/image.jpg",
      "mbti": "INTJ",
      "vote_reason": "MBTI类型理由",
      "tags": ["标签1", "标签2"]
    }
  ],
  "metadata": {
    "source": "数据来源",
    "version": "1.0",
    "upload_date": "2024-01-01"
  }
}
```

### Field Requirements

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `name` | String | Required | Celebrity's Chinese name (max 200 chars) |
| `name_en` | String | Optional | English name (max 200 chars) |
| `description` | String | Optional | Brief description |
| `image_url` | String | Optional | Image URL |
| `mbti` | String | Required | One of 16 MBTI types |
| `vote_reason` | String | Required | Reason for MBTI classification |
| `tags` | Array | Optional | List of tags |

### Valid MBTI Types

```
INTJ, INTP, ENTJ, ENTP,
INFJ, INFP, ENFJ, ENFP, 
ISTJ, ISFJ, ESTJ, ESFJ,
ISTP, ISFP, ESTP, ESFP
```

## API Endpoints

### Admin Only (Requires Authentication)

- `POST /uploads/process-pending` - Process all pending files
- `GET /uploads/status` - Get upload directory status
- `POST /uploads/upload-file` - Upload a JSON file
- `POST /uploads/validate-file` - Validate a file without processing

### Public

- `GET /uploads/schema` - Get JSON schema and examples

## Processing Workflow

1. **File Placement**: JSON files are placed in `pending/` directory
2. **Validation**: System validates JSON format and data structure
3. **Processing**: Valid files are processed and data imported to database
4. **File Movement**: 
   - Success: File moved to `processed/` with success log
   - Failure: File moved to `failed/` with error log
5. **Logging**: Detailed logs created for each operation

## Error Handling

### Validation Errors
- Invalid JSON format
- Missing required fields
- Invalid MBTI types
- Duplicate celebrity names

### Processing Errors
- Database connection issues
- System user not found
- Data integrity violations

### Error Logs
Error logs are created in the `failed/` directory with format:
```
File: filename.json
Timestamp: 2024-01-01T12:00:00
Validation Errors:
- Error 1
- Error 2
```

## Success Logs
Success logs are created in the `processed/` directory with format:
```
File: filename.json
Timestamp: 2024-01-01T12:00:00
Imported: 3 celebrities
```

## Example Usage

### 1. Create JSON File
```json
{
  "celebrities": [
    {
      "name": "周杰伦",
      "name_en": "Jay Chou",
      "description": "台湾著名歌手、音乐人、演员、导演",
      "image_url": "",
      "mbti": "INTP",
      "vote_reason": "周杰伦表现出INTP的特点：内向、理性、创新思维，在音乐创作中展现独特的逻辑性和创造力。",
      "tags": ["歌手", "音乐人", "演员", "导演", "台湾"]
    }
  ],
  "metadata": {
    "source": "MBTI分析社区",
    "version": "1.0",
    "upload_date": "2024-01-01"
  }
}
```

### 2. Place in Pending Directory
```bash
cp my_celebrities.json data_uploads/pending/
```

### 3. Process Files
```bash
curl -X POST "http://localhost:8000/uploads/process-pending" \
  -H "Authorization: Bearer YOUR_TOKEN"
```

### 4. Check Results
- Success: Check `data_uploads/processed/`
- Failure: Check `data_uploads/failed/`

## Security Notes

- All upload endpoints require admin authentication
- Files are validated before processing
- No executable files are allowed
- File size limits may apply
- Temporary files are cleaned up automatically

## Troubleshooting

### Common Issues

1. **"System user not found"**
   - Run `python create_admin.py` to create system user

2. **"Invalid JSON format"**
   - Validate JSON syntax using online tools
   - Check for missing commas, brackets, etc.

3. **"Invalid MBTI type"**
   - Use only the 16 valid MBTI types listed above

4. **"Celebrity already exists"**
   - Check database for existing celebrities
   - Use different names or update existing records

### Getting Help

- Check error logs in `failed/` directory
- Use `GET /uploads/schema` for format reference
- Validate files using `POST /uploads/validate-file`
- Check API documentation at `/docs` 