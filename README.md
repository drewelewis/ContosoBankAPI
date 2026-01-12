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

**🚀 Fresh System Setup (Recommended)**

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd ContosoBankAPI
   ```

2. **Start all services**
   ```bash
   # Windows
   _up.bat
   
   # Linux/Mac
   docker-compose up -d
   ```

3. **Set up database (automated)**
   ```bash
   # Windows - This will create database, tables, and seed test data
   _setup_database.bat
   ```

4. **Create and activate Python environment**
   ```bash
   # Windows
   _env_create.bat
   _env_activate.bat
   
   # Manual setup
   python -m venv .venv
   source .venv/bin/activate  # Linux/Mac
   .venv\Scripts\activate     # Windows
   ```

5. **Install dependencies**
   ```bash
   # Windows
   _install.bat
   
   # Manual
   pip install -r requirements.txt
   ```

6. **Start the application**
   ```bash
   # Windows
   _run_server.bat
   
   # Manual
   python main.py
   ```

7. **Access your application** 🎉
   - API Documentation: http://localhost:8000/docs
   - Database Admin: http://localhost:8082
   - Elasticsearch: http://localhost:9200
   - Kibana: http://localhost:5601

---

### Manual Setup (Alternative)

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
   DATABASE_URL="postgresql+asyncpg://postgres:postgres@localhost:5433/user_database"
   DB_HOST=localhost
   DB_PORT=5433
   DB_USER=postgres
   DB_PASSWORD=postgres
   DB_NAME=user_database
   DB_FORCE_ROLLBACK=False
   ELASTICSEARCH_HOST=localhost
   ELASTICSEARCH_PORT=9200
   ELASTICSEARCH_INDEX=contosobank-logs
   ELASTICSEARCH_LOG_LEVEL=logging.INFO
   ```

6. **Set up the database**
   ```bash
   # Windows - Automated setup (creates database, tables, and seeds data)
   _setup_database.bat
   
   # Manual steps
   python database/create_database.py  # Create database and tables
   python database/seed_database.py    # Seed with test data
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
   - Database Admin: http://localhost:8082 (Adminer)
   - Database Server: localhost:5433 (PostgreSQL - contosobank container)
   - Elasticsearch: http://localhost:9200
   - Kibana: http://localhost:5601

### 🔐 Adminer Database Connection

When accessing Adminer at http://localhost:8082, use these **exact** connection settings:

| Field | Value | Notes |
|-------|-------|-------|
| **System** | `PostgreSQL` | Select from dropdown |
| **Server** | `contosobank` | Container name (no port!) |
| **Username** | `postgres` | Database user |
| **Password** | `postgres` | Database password |
| **Database** | `user_database` | Target database |

⚠️ **Important**: 
- Use `contosobank` (container name) **not** `localhost:5433` 
- Don't include port number - Docker handles internal networking
- Ensure no trailing spaces in server field

---

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

JMeter configuration is provided for comprehensive error and performance testing:

**Test Configuration:**
- **3 concurrent threads** (simulated users)
- **3 second ramp-up time** 
- **3 loops per thread**
- **Total: 63 requests** across 7 test scenarios

**Test Scenarios:**
1. **Regular User Creation** - Baseline testing with random user data
2. **Race Condition Testing** - Multiple threads creating same username to trigger concurrency bugs
3. **Long Email Validation** - Tests validation limits with 100+ character emails
4. **Empty Password Edge Cases** - Tests null/empty string handling
5. **Memory Stress Testing** - Triggers large result sets without pagination limits
6. **Invalid UUID Testing** - Tests malformed UUID handling in endpoints
7. **Non-existent User Testing** - Tests edge cases with null UUIDs

**Run the test:**
```bash
# Run focused load test for error analysis
jmeter -n -t loadtests/test.jmx -l results.jtl

# View results in JMeter GUI
jmeter -t loadtests/test.jmx
```

**Expected Errors for Analysis:**
- `IntegrityError`: Race conditions on duplicate usernames
- `AttributeError`: Null/None value handling issues
- `ValueError`: UUID parsing and validation failures
- `MemoryError`: Large result set processing
- Various HTTP status codes: 422, 500, 404

This configuration generates realistic, organic errors perfect for AI log analysis without overwhelming the system.

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
    F -->|Yes| G[Run database/seed_database.py]
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
5. **Data Seeding**: Use `database/seed_database.py` for development data

## 📊 Monitoring & Logging

### Elasticsearch Integration

```mermaid
graph LR
    A[FastAPI App] --> B[Custom ElasticsearchHandler]
    B --> C[Console Handler]
    B --> D[Elasticsearch 9.2.3]
    D --> E[contosobank-logs Index]
    E --> F[Kibana Dashboard]
```

**Updated Architecture:**
- ✅ **Custom ElasticsearchHandler**: Direct integration with Elasticsearch 9.2.3
- ✅ **Native Elasticsearch Client**: Compatible with modern Elasticsearch versions
- ✅ **Structured Logging**: Rich log data with operation IDs and error categorization
- ✅ **Real-time Analytics**: Immediate log availability in Kibana for AI analysis

### Log Structure

The application generates structured logs perfect for AI analysis:

```json
{
  "@timestamp": "2026-01-12T12:03:33Z",
  "level": "INFO|WARNING|ERROR",
  "logger": "contosobank-logs",
  "message": "User created successfully",
  "module": "operations",
  "function": "create_user",
  "line": 73,
  "extra_data": {
    "user_id": "uuid-here",
    "operation": "user_creation",
    "operation_id": "req_abc123"
  }
}
```

### Realistic Error Patterns Generated

The JMeter load tests generate organic error patterns ideal for AI analysis:

**Database Constraint Violations:**
- String truncation errors (VARCHAR limits exceeded)
- Duplicate username conflicts from race conditions
- UUID validation failures

**Application-Level Errors:**
- Empty/null password validation
- Memory pressure from large result sets
- Malformed UUID handling

**Success Scenarios:**
- Normal user creation (201 Created)
- User retrieval requests (200 OK)
- Proper timestamp and ID generation

### Setting Up Kibana Data View

To view your application logs in Kibana for AI analysis, you need to create a data view:

1. **Open Kibana** at http://localhost:5601

2. **Navigate to Data Views**:
   - Click the hamburger menu (☰) in the top left
   - Go to **Management** → **Stack Management**
   - In the left sidebar under **Kibana**, click **Data Views**

3. **Check for New Data**:
   - Click **Check for new data** to refresh available indices
   - This will scan Elasticsearch for any new indices that have been created

4. **Create Data View**:
   - Look for a **Create data view** button or link
   - If you don't see it, try running your JMeter tests first to generate log data

5. **Configure the Data View**:
   - **Name**: `ContosoBankAPI Logs`
   - **Index pattern**: `contosobank-logs*`
   - **Timestamp field**: `@timestamp` (if available)
   - Click **Save data view to Kibana**

6. **View Your Data**:
   - Go to **Analytics** → **Discover**
   - Select your `ContosoBankAPI Logs` data view from the dropdown
   - You should now see your API logs with all the structured fields!

**✅ Verified Working**: The logging system has been tested and confirmed working with:
- Elasticsearch 9.2.3 compatibility
- Successful log ingestion from JMeter load tests
- Rich structured data including operation IDs, error types, and timing
- Realistic error/success mix perfect for AI pattern analysis

### AI Analysis Ready

Your log data is now optimized for AI analysis with:
- **Operation Correlation**: Each request has unique IDs for tracing
- **Error Categorization**: Structured error types and causes
- **Performance Metrics**: Timing data for bottleneck identification
- **Context Preservation**: Full stack traces and parameter data
- **Realistic Scenarios**: Organic errors from actual load testing

### Monitoring Endpoints

- **Application Health**: Monitor `/docs` availability
- **Database Health**: Check Adminer connection at http://localhost:8082
- **Elasticsearch Health**: Verify cluster status at http://localhost:9200/_cluster/health
- **Log Analytics**: Access structured logs via Kibana at http://localhost:5601
- **Real-time Monitoring**: Live log streaming in Kibana Discover view

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