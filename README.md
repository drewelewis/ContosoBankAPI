# ContosoBankAPI

A modern, async FastAPI-based banking application with PostgreSQL database backend, Elasticsearch logging, and comprehensive Docker support.

## 🏗️ Architecture Overview

```mermaid
graph TB
    subgraph "Client Layer"
        A[HTTP Clients]
        B[API Documentation<br>/docs]
    end
    
    subgraph "Application Layer"
        C[FastAPI Application<br>main.py]
        D[User Operations<br>operations.py]
        E[Database Models<br>models.py]
        F[Configuration<br>config.py]
        G[Logging Service<br>logger.py]
    end
    
    subgraph "Database Layer"
        H[PostgreSQL<br>Database]
        I[Elasticsearch<br>Logs]
    end
    
    subgraph "Infrastructure"
        J[Docker Compose<br>Services]
        K[Adminer<br>DB Admin]
        L[Kibana<br>Log Visualization]
    end
    
    A --> C
    B --> C
    C --> D
    C --> E
    C --> F
    C --> G
    D --> H
    G --> I
    J --> H
    J --> I
    J --> K
    J --> L
```

## 📋 Table of Contents

- [Features](#features)
- [Technology Stack](#technology-stack)
- [Getting Started](#getting-started)
- [API Endpoints](#api-endpoints)
- [Database Schema](#database-schema)
- [Docker Services](#docker-services)
- [Environment Configuration](#environment-configuration)
- [Testing](#testing)
- [Development Workflow](#development-workflow)
- [Monitoring & Logging](#monitoring--logging)
- [Troubleshooting](#troubleshooting)

## ✨ Features

- **Modern FastAPI Framework**: High-performance async API with automatic documentation
- **User Management**: Complete CRUD operations for user accounts
- **Secure Authentication**: Password hashing with bcrypt
- **Database Integration**: PostgreSQL with SQLAlchemy ORM and async support
- **Centralized Logging**: Elasticsearch integration with Kibana visualization
- **Containerized Infrastructure**: Docker Compose for easy deployment
- **Database Administration**: Adminer web interface for database management
- **Data Seeding**: Automated user data generation with Faker
- **Load Testing**: JMeter configuration for performance testing
- **Development Tools**: Batch scripts for easy environment management

## 🛠️ Technology Stack

### Backend
- **FastAPI**: Modern web framework for building APIs
- **SQLAlchemy 2.0+**: Async ORM with PostgreSQL support
- **Pydantic**: Data validation and settings management
- **bcrypt**: Password hashing and verification
- **asyncpg**: Async PostgreSQL driver

### Database & Storage
- **PostgreSQL 17.5**: Primary database with UUID and crypto extensions
- **Elasticsearch 7.15**: Log storage and indexing

### Infrastructure
- **Docker & Docker Compose**: Containerized development environment
- **Uvicorn**: ASGI server for FastAPI
- **Adminer**: Database administration interface
- **Kibana**: Log visualization and analysis

### Development & Testing
- **Faker**: Test data generation
- **pytest**: Testing framework with async support
- **JMeter**: Load testing configuration
- **Alembic**: Database migrations

## 🚀 Getting Started

### Prerequisites

- Python 3.9+
- Docker and Docker Compose
- Git

### Quick Start

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd ContosoBankAPI
   ```

2. **Start Docker services**
   ```bash
   # Windows
   _up.bat
   
   # Linux/Mac
   docker-compose up -d
   ```

3. **Create Python environment**
   ```bash
   # Windows
   _env_create.bat
   _env_activate.bat
   
   # Manual setup
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   venv\Scripts\activate     # Windows
   ```

4. **Install dependencies**
   ```bash
   # Windows
   _install.bat
   
   # Manual
   pip install -r requirements.txt
   ```

5. **Set up environment variables**
   Create a `.env` file in the root directory:
   ```env
   DATABASE_URL=postgresql+asyncpg://postgres:postgres@localhost:5432/postgres
   ELASTICSEARCH_HOST=localhost
   ELASTICSEARCH_PORT=9200
   ELASTICSEARCH_INDEX=contosobank-logs
   ELASTICSEARCH_LOG_LEVEL=DEBUG
   ```

6. **Seed the database** (Optional)
   ```bash
   python seed_database.py
   ```

7. **Start the application**
   ```bash
   # Windows
   _run_server.bat
   
   # Manual
   python main.py
   ```

8. **Access the application**
   - API Documentation: http://localhost:8000/docs
   - Database Admin: http://localhost:8080
   - Elasticsearch: http://localhost:9200
   - Kibana: http://localhost:5601

## 📚 API Endpoints

### User Management

```mermaid
sequenceDiagram
    participant Client
    participant FastAPI
    participant Database
    participant Logger

    Client->>FastAPI: POST /users/
    FastAPI->>Database: Create user with hashed password
    Database-->>FastAPI: Return user object
    FastAPI->>Logger: Log operation
    FastAPI-->>Client: Return created user

    Client->>FastAPI: GET /users/{user_id}
    FastAPI->>Database: Query user by ID
    Database-->>FastAPI: Return user or null
    FastAPI->>Logger: Log operation
    FastAPI-->>Client: Return user or 404

    Client->>FastAPI: GET /users/
    FastAPI->>Database: Query all users
    Database-->>FastAPI: Return users list
    FastAPI->>Logger: Log operation
    FastAPI-->>Client: Return users array
```

### Endpoints

| Method | Endpoint | Description | Request Body | Response |
|--------|----------|-------------|--------------|----------|
| `GET` | `/` | Redirect to API docs | - | Redirect to `/docs` |
| `POST` | `/users/` | Create a new user | `UserCreateModel` | Created user object |
| `GET` | `/users/{user_id}` | Get user by ID | - | User object or 404 |
| `GET` | `/users/` | Get all users | - | Array of user objects |

### Request/Response Models

**UserCreateModel**
```json
{
  "first_name": "string",
  "last_name": "string",
  "email": "user@example.com",
  "username": "string",
  "password_hash": "string"
}
```

**User Response**
```json
{
  "user_id": "uuid",
  "first_name": "string",
  "last_name": "string",
  "email": "user@example.com",
  "username": "string",
  "password_hash": "hashed_string",
  "created_at": "2026-01-06T12:00:00Z",
  "updated_at": null,
  "deleted_at": null
}
```

## 🗄️ Database Schema

```mermaid
erDiagram
    USERS {
        uuid user_id PK
        varchar first_name
        varchar last_name
        varchar email
        varchar username
        varchar password_hash
        timestamp created_at
        timestamp updated_at
        timestamp deleted_at
    }
```

### Database Features

- **UUID Primary Keys**: Globally unique identifiers for all records
- **Audit Trail**: Created, updated, and deleted timestamps
- **Password Security**: bcrypt hashing for all passwords
- **Indexes**: Optimized queries on user_id and email
- **Extensions**: PostgreSQL pgcrypto and uuid-ossp extensions

### Database Indexes

```sql
CREATE INDEX idx_users_email ON users (email);
CREATE INDEX idx_users_user_id ON users (user_id);
```

## 🐳 Docker Services

```mermaid
graph LR
    subgraph "Docker Compose Services"
        A[PostgreSQL<br>:5432]
        B[Adminer<br>:8080]
        C[Elasticsearch<br>:9200]
        D[Kibana<br>:5601]
        E[FastAPI App<br>:8000]
    end
    
    E --> A
    E --> C
    B --> A
    D --> C
```

### Service Configuration

| Service | Port | Purpose | Dependencies |
|---------|------|---------|-------------|
| **PostgreSQL** | 5432 | Primary database | - |
| **Adminer** | 8080 | Database administration | PostgreSQL |
| **Elasticsearch** | 9200 | Log storage and indexing | - |
| **Kibana** | 5601 | Log visualization | Elasticsearch |
| **FastAPI** | 8000 | Main application | PostgreSQL, Elasticsearch |

### Docker Volumes

- `postgres_data`: Persistent PostgreSQL data
- `elasticsearch_data`: Persistent Elasticsearch data

## ⚙️ Environment Configuration

### Required Environment Variables

```env
# Database Configuration
DATABASE_URL=postgresql+asyncpg://postgres:postgres@localhost:5432/postgres
DB_FORCE_ROLLBACK=false

# Elasticsearch Configuration
ELASTICSEARCH_HOST=localhost
ELASTICSEARCH_PORT=9200
ELASTICSEARCH_INDEX=contosobank-logs
ELASTICSEARCH_LOG_LEVEL=DEBUG
```

### Configuration Management

The application uses Pydantic Settings for configuration management:

- Environment variables from `.env` file
- Type validation and parsing
- Optional settings with defaults
- Cached configuration loading

## 🧪 Testing

### Load Testing

JMeter configuration is provided for performance testing:

```bash
# Run load tests
jmeter -n -t loadtests/test1.jmx -l results.jtl
```

### Database Testing

```bash
# Run with test database
pytest tests/
```

### Manual Testing

Use the interactive API documentation at http://localhost:8000/docs to test endpoints manually.

## 🔄 Development Workflow

```mermaid
flowchart TD
    A[Start Development] --> B[Run _up.bat]
    B --> C[Activate Environment]
    C --> D[Start Application]
    D --> E[Develop & Test]
    E --> F{Need Data?}
    F -->|Yes| G[Run seed_database.py]
    F -->|No| H[Continue Development]
    G --> H
    H --> I[Test Changes]
    I --> J{Deploy?}
    J -->|Yes| K[Build & Deploy]
    J -->|No| E
    K --> L[Monitor Logs]
```

### Batch Scripts (Windows)

- `_up.bat`: Start all Docker services
- `_down.bat`: Stop all Docker services
- `_env_create.bat`: Create Python virtual environment
- `_env_activate.bat`: Activate virtual environment
- `_env_deactivate.bat`: Deactivate virtual environment
- `_install.bat`: Install Python dependencies
- `_run_server.bat`: Start the FastAPI application

### Development Best Practices

1. **Environment Management**: Always use virtual environments
2. **Database Migrations**: Use Alembic for schema changes
3. **Logging**: Monitor application logs in Kibana
4. **Testing**: Test endpoints using `/docs` interface
5. **Data Seeding**: Use `seed_database.py` for development data

## 📊 Monitoring & Logging

### Elasticsearch Integration

```mermaid
graph LR
    A[FastAPI App] --> B[Logger Module]
    B --> C[Console Handler]
    B --> D[Elasticsearch Handler]
    D --> E[Elasticsearch Index]
    E --> F[Kibana Dashboard]
```

### Log Structure

```json
{
  "@timestamp": "2026-01-06T12:00:00Z",
  "level": "INFO",
  "logger": "contosobank-logs",
  "message": "User created successfully",
  "module": "operations",
  "function": "create_user",
  "extra_data": {
    "user_id": "uuid-here",
    "operation": "user_creation"
  }
}
```

### Monitoring Endpoints

- **Application Health**: Monitor `/docs` availability
- **Database Health**: Check Adminer connection
- **Elasticsearch Health**: Verify index creation in Kibana

## 🔧 Troubleshooting

### Common Issues

**Database Connection Error**
```bash
# Check if PostgreSQL is running
docker ps | grep postgres

# Check connection string
echo $DATABASE_URL
```

**Elasticsearch Not Responding**
```bash
# Check Elasticsearch status
curl http://localhost:9200/_health

# Restart Elasticsearch
docker-compose restart elasticsearch
```

**Port Conflicts**
```bash
# Check what's using ports
netstat -tulpn | grep :8000
netstat -tulpn | grep :5432

# Stop conflicting services
docker-compose down
```

### Debug Mode

Enable debug logging by setting:
```env
ELASTICSEARCH_LOG_LEVEL=DEBUG
```

### Performance Issues

1. Monitor database queries in logs
2. Check Elasticsearch index size
3. Review JMeter test results
4. Monitor Docker container resources

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

[Add your license information here]

## 📞 Support

For support and questions:
- Check the troubleshooting section
- Review application logs in Kibana
- Monitor database with Adminer
- Use the interactive API docs at `/docs`

---

**Happy Banking! 🏦**