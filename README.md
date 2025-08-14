# 16型花名册 (MBTI Roster)

A FastAPI-based web application for voting on celebrities' MBTI personality types.

## Features

- **User Authentication**: Registration and login with JWT tokens
- **Enhanced Error Handling**: Detailed, actionable error messages for better UX
- **Celebrity Management**: CRUD operations for celebrity profiles
- **Voting System**: Vote on celebrities' MBTI personality types (16 types)
- **Comment System**: Nested comments for discussions
- **Tag System**: Categorize celebrities with tags
- **Vote Limits**: Daily vote limits and reason requirements
- **Admin Panel**: Manage users and content with role-based access control
- **CI/CD Pipeline**: Automated testing, building, and deployment
- **Docker Support**: Multi-stage builds for development and production
- **Code Quality**: Automated linting, formatting, and security scanning

## Development Guidelines

Before contributing to this project, please read our [Development Guidelines](DEVELOPMENT_GUIDELINES.md) which include:
- **Emoji Usage Policy**: No emojis allowed in code, documentation, or any project files
- **Code Quality Standards**: Black formatting, Flake8 linting, MyPy type checking
- **Testing Requirements**: Unit and integration test coverage
- **Git Workflow**: Commit message conventions and branch naming
- **CI/CD Pipeline**: Automated quality checks and deployment

## Quick Start

### Prerequisites
- Python 3.8+ (Tested with Python 3.13)
- SQLite (for development) / PostgreSQL (for production)
- Redis (optional for development)

### Installation

#### Option 1: Automated Setup (Recommended)
```bash
# Clone the repository
git clone https://github.com/Linnnnberg/16TypeDatabaseCN.git
cd 16TypeDatabaseCN

# Create virtual environment
python -m venv venv

# Run automated setup
python dev_setup.py --full
```

#### Option 2: Manual Setup
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

### Development Commands

#### Quick Server Startup (Windows PowerShell)
```powershell
.\start_dev.ps1
```

#### Development Script Commands
```bash
# Full setup (environment, dependencies, sample data, server)
python dev_setup.py --full

# Start server only
python dev_setup.py --server

# Test endpoints only
python dev_setup.py --test

# Create sample data only
python dev_setup.py --data

# Show development information
python dev_setup.py --info
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

## CI/CD Pipeline

This project includes a comprehensive CI/CD pipeline for automated testing, building, and deployment.

### Pipeline Features
- **Automated Testing**: Unit tests, integration tests, and code quality checks
- **Security Scanning**: Bandit for code security, Safety for dependency vulnerabilities
- **Code Quality**: Black formatting, Flake8 linting, MyPy type checking
- **Docker Builds**: Multi-stage builds for development and production
- **Automated Deployment**: Staging deployment on main branch, manual production deployment
- **Documentation**: Automatic API documentation generation

### Pipeline Jobs
1. **Test & Quality Check**: Code formatting, linting, type checking, security scanning
2. **Integration Tests**: End-to-end testing with running application
3. **Build**: Docker image building and caching
4. **Security Scan**: Trivy vulnerability scanning
5. **Deploy Staging**: Automatic deployment to staging environment
6. **Documentation**: Generate and upload API documentation

### Local Development with Docker
```bash
# Start development environment
docker-compose up -d

# Run tests
docker-compose --profile test up test

# Performance testing
docker-compose --profile performance up locust

# Monitoring
docker-compose --profile monitoring up -d
```

For detailed CI/CD documentation, see [CI_CD_COMPREHENSIVE.md](CI_CD_COMPREHENSIVE.md).

## Development

### Current Status
- **Phase 1**: Project setup and foundation - **COMPLETED**
- **Phase 2**: Authentication system - **COMPLETED**
- **Phase 3**: Celebrity management and voting system - **COMPLETED**
- **CI/CD Pipeline**: Automated testing and deployment - **COMPLETED**
- **Phase 4**: User experience enhancement - **NEXT PRIORITY**

### Features Implemented
- User authentication with JWT tokens
- Enhanced error handling with detailed, actionable messages
- Password hashing with bcrypt
- User registration and login
- Role-based access control (SYSTEM/CLIENT)
- Database models and relationships
- Pydantic schemas for validation
- API documentation with Swagger UI
- Celebrity management system (CRUD operations)
- Voting system with daily limits
- Comment system with nested replies
- Tag system for categorization
- Frontend interface (FastAPI + Jinja2 + Tailwind CSS)
- CI/CD pipeline with automated testing and deployment
- Docker containerization for development and production

### Next Steps
- User experience enhancement (loading states, notifications)
- Search functionality re-implementation
- Advanced features (analytics, monitoring)
- Production deployment preparation

See [TODO.md](TODO.md) for detailed development tasks and roadmap.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.