#!/usr/bin/env python3
"""
Script to create .env file with proper UTF-8 encoding
"""

def create_env_file():
    """Create .env file with proper encoding"""
    env_content = """# Database Configuration (SQLite for local development)
DATABASE_URL=sqlite:///./mbti_roster.db

# Security
SECRET_KEY=your-super-secret-key-here-change-this-in-production

# Redis Configuration
REDIS_URL=redis://localhost:6379

# Email Configuration
EMAIL_FROM=noreply@mbti-roster.com

# Voting Limits
DAILY_VOTE_LIMIT=20
DAILY_NO_REASON_LIMIT=5
NEW_USER_24H_LIMIT=3
DAILY_REGISTRATIONS_PER_IP=3
"""
    
    with open('.env', 'w', encoding='utf-8') as f:
        f.write(env_content)
    
    print(".env file created successfully with UTF-8 encoding")

if __name__ == "__main__":
    create_env_file() 