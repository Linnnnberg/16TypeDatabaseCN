# API Documentation - 16型花名册 (MBTI Roster)

## Overview

The 16型花名册 API is a RESTful service built with FastAPI for managing celebrity MBTI personality type voting. The API uses JWT tokens for authentication and provides comprehensive endpoints for user management, celebrity data, voting, and comments.

## Base URL

- **Development**: `http://localhost:8000`
- **API Documentation**: `http://localhost:8000/docs`
- **Health Check**: `http://localhost:8000/health`

## Authentication

The API uses JWT (JSON Web Tokens) for authentication. Include the token in the Authorization header:

```
Authorization: Bearer <your_jwt_token>
```

### Token Format
- **Type**: JWT
- **Algorithm**: HS256
- **Expiration**: 24 hours
- **Payload**: Contains user ID and email

## Endpoints

### MBTI Types Endpoints

#### Get All MBTI Types
```http
GET /api/mbti/types
```

**Response:**
```json
{
  "types": [
    {
      "code": "INTJ",
      "chinese_name": "建筑师",
      "english_name": "Architect",
      "description": "富有想象力和战略性的思考者，一切都要经过深思熟虑"
    },
    {
      "code": "INTP",
      "chinese_name": "逻辑学家",
      "english_name": "Logician",
      "description": "具有创新想法和独特见解的发明家"
    }
  ],
  "total": 16,
  "message": "MBTI types retrieved successfully"
}
```

#### Get Specific MBTI Type
```http
GET /api/mbti/types/{type_code}
```

**Parameters:**
- `type_code` (string): The MBTI type code (e.g., "INTJ", "ENFP")

**Response:**
```json
{
  "code": "INTJ",
  "chinese_name": "建筑师",
  "english_name": "Architect",
  "description": "富有想象力和战略性的思考者，一切都要经过深思熟虑"
}
```

#### Get MBTI Types List
```http
GET /api/mbti/types-list
```

**Response:**
```json
{
  "types": ["INTJ", "INTP", "ENTJ", "ENTP", "INFJ", "INFP", "ENFJ", "ENFP", "ISTJ", "ISFJ", "ESTJ", "ESFJ", "ISTP", "ISFP", "ESTP", "ESFP"],
  "total": 16,
  "message": "MBTI type codes retrieved successfully"
}
```

#### Validate MBTI Type
```http
GET /api/mbti/validate/{type_code}
```

**Parameters:**
- `type_code` (string): The MBTI type code to validate

**Response:**
```json
{
  "type_code": "INTJ",
  "is_valid": true,
  "message": "MBTI type INTJ is valid"
}
```

### Authentication Endpoints

#### Register User
```http
POST /auth/signup
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "password123",
  "name": "John Doe"
}
```

**Response:**
```json
{
  "id": "uuid-string",
  "email": "user@example.com",
  "name": "John Doe",
  "role": "CLIENT",
  "is_active": true,
  "created_at": "2025-08-04T17:35:32"
}
```

#### Login User
```http
POST /auth/login
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "password123"
}
```

**Response:**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "expires_in": 86400
}
```

#### Get Current User Profile
```http
GET /auth/me
Authorization: Bearer <token>
```

**Response:**
```json
{
  "id": "uuid-string",
  "email": "user@example.com",
  "name": "John Doe",
  "role": "CLIENT",
  "is_active": true,
  "created_at": "2025-08-04T17:35:32",
  "updated_at": null
}
```

#### Update User Profile
```http
PUT /auth/me
Authorization: Bearer <token>
Content-Type: application/json

{
  "name": "John Smith"
}
```

#### Deactivate User Account
```http
DELETE /auth/me
Authorization: Bearer <token>
```

### Admin Endpoints

#### Create System User (Admin Only)
```http
POST /auth/admin/create-system-user
Authorization: Bearer <admin_token>
Content-Type: application/json

{
  "email": "admin2@example.com",
  "password": "admin123",
  "name": "Admin User"
}
```

## Data Models

### User Model
```json
{
  "id": "string (UUID)",
  "email": "string (email)",
  "name": "string (1-100 chars)",
  "role": "SYSTEM | CLIENT",
  "is_active": "boolean",
  "created_at": "datetime",
  "updated_at": "datetime | null"
}
```

### MBTI Types
The system supports all 16 MBTI personality types:
- **Analysts**: INTJ, INTP, ENTJ, ENTP
- **Diplomats**: INFJ, INFP, ENFJ, ENFP
- **Sentinels**: ISTJ, ISFJ, ESTJ, ESFJ
- **Explorers**: ISTP, ISFP, ESTP, ESFP

## Error Responses

### Standard Error Format
```json
{
  "detail": "Error message description"
}
```

### Common HTTP Status Codes
- `200` - Success
- `201` - Created
- `400` - Bad Request
- `401` - Unauthorized
- `403` - Forbidden
- `404` - Not Found
- `422` - Validation Error
- `500` - Internal Server Error

### Example Error Responses

#### Validation Error (422)
```json
{
  "detail": [
    {
      "loc": ["body", "email"],
      "msg": "field required",
      "type": "value_error.missing"
    }
  ]
}
```

#### Authentication Error (401)
```json
{
  "detail": "Could not validate credentials"
}
```

#### Duplicate Email (400)
```json
{
  "detail": "Email already registered"
}
```

## Rate Limiting

Currently, no rate limiting is implemented. Future versions will include:
- Daily vote limits per user
- Registration limits per IP
- API request rate limiting

## Development

### Testing the API

1. **Start the server**:
   ```bash
   python run_local.py
   ```

2. **Create an admin user**:
   ```bash
   python create_admin.py
   ```

3. **Test endpoints**:
   - Visit `http://localhost:8000/docs` for interactive API documentation
   - Use the Swagger UI to test endpoints directly
   - Use tools like curl, Postman, or Insomnia

### Default Admin Credentials
- **Email**: admin@mbti-roster.com
- **Password**: admin123

## Future Endpoints

The following endpoints are planned for future implementation:

### Celebrity Management
- `GET /celebrities` - List celebrities
- `POST /celebrities` - Create celebrity
- `GET /celebrities/{id}` - Get celebrity details
- `PUT /celebrities/{id}` - Update celebrity
- `DELETE /celebrities/{id}` - Delete celebrity

### Voting System
- `POST /votes` - Create vote
- `GET /votes` - List votes
- `GET /votes/{id}` - Get vote details
- `DELETE /votes/{id}` - Delete vote

### Comment System
- `POST /comments` - Create comment
- `GET /comments` - List comments
- `PUT /comments/{id}` - Update comment
- `DELETE /comments/{id}` - Delete comment

### Tag System
- `GET /tags` - List tags
- `POST /tags` - Create tag
- `GET /tags/{id}` - Get tag details

## Support

For issues and questions:
1. Check the interactive API documentation at `/docs`
2. Review the project's TODO.md for development status
3. Check the server logs for detailed error information 