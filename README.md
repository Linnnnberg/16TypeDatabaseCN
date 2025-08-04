# 16型花名册 (MBTI Roster)

A FastAPI-based web application for voting on celebrities' MBTI personality types.

## Features

- **User Authentication**: Registration and login with JWT tokens
- **Celebrity Management**: CRUD operations for celebrity profiles
- **Voting System**: Vote on celebrities' MBTI personality types (16 types)
- **Comment System**: Nested comments for discussions
- **Tag System**: Categorize celebrities with tags
- **Vote Limits**: Daily vote limits and reason requirements
- **Admin Panel**: Manage users and content

## Quick Start

### Prerequisites
- Python 3.8+ (Tested with Python 3.13)
- SQLite (for development) / PostgreSQL (for production)
- Redis (optional for development)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/Linnnnberg/16TypeDatabaseCN.git
   cd 16TypeDatabaseCN
   ```

2. **Set up virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements_minimal.txt
   ```

4. **Configure environment**
   ```bash
   python create_env.py  # Creates .env file with proper encoding
   ```

5. **Create admin user (optional)**
   ```bash
   python create_admin.py
   ```

6. **Run the application**
   ```bash
   python run_local.py
   ```

   Or directly with uvicorn:
   ```bash
   venv\Scripts\uvicorn.exe app.main:app --reload
   ```

## API Documentation

Once running, visit:
- **API Docs**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/health
- **Test Endpoint**: http://localhost:8000/test

### Authentication Endpoints
- `POST /auth/signup` - Register new user
- `POST /auth/login` - Login and get JWT token
- `GET /auth/me` - Get current user profile
- `PUT /auth/me` - Update user profile
- `DELETE /auth/me` - Deactivate user account

### Default Admin User
- **Email**: admin@mbti-roster.com
- **Password**: admin123
- **Role**: SYSTEM (admin privileges)

## Project Structure

```
16TypeDatabaseCN/
├── app/
│   ├── api/          # API endpoints
│   ├── core/         # Configuration and utilities
│   ├── database/     # Database models and connection
│   ├── schemas/      # Pydantic models
│   ├── services/     # Business logic
│   └── main.py       # FastAPI application
├── static/           # Static files
├── templates/        # HTML templates
├── alembic/          # Database migrations
├── requirements.txt  # Python dependencies
├── run.py           # Startup script
└── TODO.md          # Development tasks
```

## Development

### Current Status
- ✅ **Phase 1**: Project setup and foundation - **COMPLETED**
- ✅ **Phase 2**: Authentication system - **COMPLETED**
- 🔄 **Phase 3**: Celebrity management and voting system - **IN PROGRESS**

### Features Implemented
- ✅ User authentication with JWT tokens
- ✅ Password hashing with bcrypt
- ✅ User registration and login
- ✅ Role-based access control (SYSTEM/CLIENT)
- ✅ Database models and relationships
- ✅ Pydantic schemas for validation
- ✅ API documentation with Swagger UI

### Next Steps
- 🔄 Celebrity management endpoints
- 🔄 Voting system implementation
- 🔄 Comment system
- 🔄 Frontend interface

See [TODO.md](TODO.md) for detailed development tasks and roadmap.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
