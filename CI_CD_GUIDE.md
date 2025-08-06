# CI/CD Pipeline Guide - MBTI Roster

## Overview

This document describes the comprehensive CI/CD (Continuous Integration/Continuous Deployment) pipeline for the MBTI Roster application. The pipeline ensures code quality, security, and reliable deployments.

## Pipeline Architecture

### **Pipeline Stages**

```
Code Push → Test → Quality Check → Build → Security Scan → Deploy → Monitor
    ↓         ↓         ↓          ↓         ↓           ↓        ↓
  Trigger   Unit     Linting    Docker   Security   Staging   Health
  Pipeline  Tests    & Types    Image    Scan       Deploy    Checks
```

### **GitHub Actions Workflow**

The pipeline is defined in `.github/workflows/ci.yml` and includes:

1. **Test & Quality Check** - Unit tests, linting, type checking
2. **Integration Tests** - End-to-end testing
3. **Build** - Docker image creation
4. **Security Scan** - Vulnerability scanning
5. **Deploy to Staging** - Automatic deployment to staging
6. **Deploy to Production** - Manual deployment to production
7. **Performance Tests** - Load testing
8. **Documentation** - Auto-generated docs

## Local Development Setup

### **Prerequisites**

```bash
# Install Docker and Docker Compose
# Install Python 3.13
# Install pre-commit hooks
pip install pre-commit
pre-commit install
```

### **Quick Start**

```bash
# Start development environment
docker-compose up -d

# Run tests locally
docker-compose --profile test up test

# Run performance tests
docker-compose --profile performance up locust

# Run with monitoring
docker-compose --profile monitoring up -d
```

### **Development Commands**

```bash
# Format code
black app/ tests/

# Lint code
flake8 app/ tests/

# Type check
mypy app/

# Run tests
pytest tests/ -v

# Run with coverage
pytest tests/ --cov=app --cov-report=html

# Security scan
bandit -r app/
safety check

# Performance test
locust -f performance_tests/locustfile.py --host=http://localhost:8000
```

## Pipeline Configuration

### **Environment Variables**

Create `.env` files for different environments:

```bash
# .env.development
DATABASE_URL=sqlite:///./mbti_roster.db
SECRET_KEY=dev-secret-key
DEBUG=true
LOG_LEVEL=DEBUG

# .env.production
DATABASE_URL=postgresql://user:pass@db:5432/mbti_roster
SECRET_KEY=your-production-secret-key
DEBUG=false
LOG_LEVEL=INFO
```

### **Docker Configuration**

The application uses multi-stage Docker builds:

- **Base**: Common dependencies
- **Development**: Development tools and hot reload
- **Production**: Optimized for production
- **Testing**: Testing tools and frameworks

### **Docker Compose Profiles**

```bash
# Development
docker-compose up -d

# Testing
docker-compose --profile test up test

# Performance testing
docker-compose --profile performance up locust

# Monitoring
docker-compose --profile monitoring up -d

# Production-like
docker-compose --profile production up -d
```

## Testing Strategy

### **Test Types**

1. **Unit Tests** - Individual function/class testing
2. **Integration Tests** - API endpoint testing
3. **End-to-End Tests** - Full user workflow testing
4. **Performance Tests** - Load and stress testing
5. **Security Tests** - Vulnerability scanning

### **Test Structure**

```
tests/
├── unit/           # Unit tests
├── integration/    # Integration tests
├── e2e/           # End-to-end tests
├── performance/   # Performance tests
├── fixtures/      # Test data
└── conftest.py    # Test configuration
```

### **Running Tests**

```bash
# All tests
pytest tests/

# Specific test type
pytest tests/unit/
pytest tests/integration/

# With coverage
pytest tests/ --cov=app --cov-report=html

# Performance tests
locust -f tests/performance/locustfile.py
```

## 🔒 Security

### **Security Tools**

- **Bandit** - Python security linting
- **Safety** - Dependency vulnerability scanning
- **Trivy** - Container vulnerability scanning
- **Pre-commit hooks** - Pre-commit security checks

### **Security Checks**

```bash
# Code security scan
bandit -r app/

# Dependency security scan
safety check

# Container security scan
trivy image mbti-roster:latest

# Pre-commit security hooks
pre-commit run --all-files
```

## Monitoring & Observability

### **Monitoring Stack**

- **Prometheus** - Metrics collection
- **Grafana** - Visualization and dashboards
- **Health Checks** - Application health monitoring
- **Logging** - Structured logging with structlog

### **Key Metrics**

- Application response time
- Error rates
- Database performance
- Resource utilization
- User activity

### **Accessing Monitoring**

```bash
# Prometheus
http://localhost:9090

# Grafana
http://localhost:3000
# Username: admin
# Password: admin
```

## Deployment

### **Deployment Environments**

1. **Development** - Local development
2. **Staging** - Pre-production testing
3. **Production** - Live application

### **Deployment Process**

#### **Staging Deployment (Automatic)**
- Triggered on push to `main` branch
- Runs all tests and quality checks
- Deploys to staging environment
- Runs smoke tests

#### **Production Deployment (Manual)**
- Requires manual approval
- Runs comprehensive testing
- Deploys to production
- Runs health checks

### **Deployment Commands**

```bash
# Deploy to staging
git push origin main  # Triggers automatic staging deployment

# Deploy to production
# Go to GitHub Actions → Deploy to Production → Run workflow
```

## Performance Testing

### **Performance Test Types**

1. **Load Testing** - Normal expected load
2. **Stress Testing** - Beyond normal capacity
3. **Spike Testing** - Sudden traffic spikes
4. **Endurance Testing** - Long-term stability

### **Performance Metrics**

- Response time (p50, p95, p99)
- Throughput (requests/second)
- Error rate
- Resource utilization

### **Running Performance Tests**

```bash
# Start application
docker-compose up -d

# Run Locust performance tests
docker-compose --profile performance up locust

# Access Locust UI
http://localhost:8089
```

## Continuous Integration

### **CI Triggers**

- Push to any branch
- Pull request creation/update
- Manual workflow dispatch

### **CI Stages**

1. **Code Quality** - Formatting, linting, type checking
2. **Security** - Vulnerability scanning
3. **Testing** - Unit and integration tests
4. **Build** - Docker image creation
5. **Deploy** - Staging deployment

### **CI Best Practices**

- Keep builds fast (< 10 minutes)
- Fail fast on errors
- Cache dependencies
- Parallel job execution
- Comprehensive test coverage

## Documentation

### **Auto-Generated Documentation**

- API documentation (pdoc3)
- Code coverage reports
- Test reports
- Performance reports

### **Manual Documentation**

- README.md
- API_DOCUMENTATION.md
- DEPLOYMENT_GUIDE.md
- TROUBLESHOOTING.md

## Troubleshooting

### **Common Issues**

#### **Pipeline Failures**

```bash
# Check pipeline status
# Go to GitHub Actions tab

# View detailed logs
# Click on failed job for details

# Common fixes:
# - Fix linting errors
# - Update dependencies
# - Fix test failures
```

#### **Local Development Issues**

```bash
# Reset Docker environment
docker-compose down -v
docker-compose up -d

# Check logs
docker-compose logs app

# Rebuild images
docker-compose build --no-cache
```

#### **Test Failures**

```bash
# Run tests with verbose output
pytest tests/ -v -s

# Run specific failing test
pytest tests/test_specific.py::test_function -v

# Check test coverage
pytest tests/ --cov=app --cov-report=term-missing
```

### **Performance Issues**

```bash
# Check resource usage
docker stats

# Monitor application logs
docker-compose logs -f app

# Run performance tests
locust -f performance_tests/locustfile.py
```

## Best Practices

### **Code Quality**

- Write comprehensive tests
- Use type hints
- Follow PEP 8 style guide
- Document functions and classes
- Keep functions small and focused

### **Security**

- Never commit secrets
- Use environment variables
- Regular dependency updates
- Security scanning in CI/CD
- Principle of least privilege

### **Performance**

- Monitor key metrics
- Optimize database queries
- Use caching where appropriate
- Load test before deployment
- Monitor resource usage

### **Deployment**

- Use blue-green deployments
- Rollback capability
- Health checks
- Monitoring and alerting
- Backup strategies

## 🔗 Useful Links

- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [Docker Documentation](https://docs.docker.com/)
- [Pytest Documentation](https://docs.pytest.org/)
- [Locust Documentation](https://docs.locust.io/)
- [Prometheus Documentation](https://prometheus.io/docs/)
- [Grafana Documentation](https://grafana.com/docs/)

---

**Last Updated**: August 4, 2025  
**Pipeline Version**: 1.0  
**Maintained By**: Development Team 