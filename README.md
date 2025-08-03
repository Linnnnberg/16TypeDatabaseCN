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
- Python 3.8+
- PostgreSQL
- Redis

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
   pip install -r requirements.txt
   ```

4. **Configure environment**
   ```bash
   cp env.example .env
   # Edit .env with your database credentials
   ```

5. **Run the application**
   ```bash
   python run.py
   ```

   Or directly with uvicorn:
   ```bash
   uvicorn app.main:app --reload
   ```

## API Documentation

Once running, visit:
- **API Docs**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/health

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

See [TODO.md](TODO.md) for development tasks and roadmap.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
