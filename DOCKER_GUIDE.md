# Docker Setup & Testing Guide for Pramith API

## 🚀 Quick Start

### Prerequisites
- Docker installed ([Download Docker Desktop](https://www.docker.com/products/docker-desktop))
- `.env` file configured with your database credentials

### 1. **Build and Run API**

```bash
# Build the Docker image
docker build -t pramith-api:latest .

# Run with docker-compose (Recommended)
docker-compose up -d api

# Or run directly
docker run -p 8000:8000 --env-file .env pramith-api:latest
```

### 2. **View Logs**

```bash
# View real-time logs
docker-compose logs -f api

# Or view logs from a specific container
docker logs pramith-api -f
```

### 3. **Stop and Clean Up**

```bash
# Stop all services
docker-compose down

# Remove containers and volumes
docker-compose down -v

# Stop specific container
docker stop pramith-api
```

---

## 🧪 API Testing Options

### Option 1: Quick Health Check

```bash
# Check if API is running
curl http://localhost:8000/health

# Check auth service
curl http://localhost:8000/api/auth/health
```

### Option 2: Test with Python Script (Docker)

```bash
# Run comprehensive tests in Docker
docker-compose run --rm tests

# Or run specific pytest file
docker-compose run --rm tests pytest test_user_api.py -v
```

### Option 3: Test with Our Custom Test Script

```bash
# Run inside Docker
docker-compose exec api python api_test_docker.py

# Or run locally (requires API running)
python api_test_docker.py
```

### Option 4: Manual Testing with cURL

```bash
# Register a user
curl -X POST http://localhost:8000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "name": "John Doe",
    "mobile": "+919876543210",
    "email": "john@example.com",
    "password": "securePassword123",
    "username": "johndoe",
    "role": "patient"
  }'

# Login
curl -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "username": "johndoe",
    "password": "securePassword123"
  }'

# List users (with authorization if needed)
curl -X GET http://localhost:8000/api/users

# Create a user
curl -X POST http://localhost:8000/api/users \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Alice Smith",
    "mobile": "+919876543211",
    "email": "alice@example.com",
    "password": "password123",
    "role": "patient"
  }'
```

### Option 5: Testing with Postman/Insomnia

1. Import endpoints from `API_ENDPOINTS_WITH_EXAMPLES.md`
2. Set base URL to `http://localhost:8000`
3. Add environment variable: `BASE_URL=http://localhost:8000`

---

## 🔧 Environment Variables - Parameter Passing

### Via Docker Compose (Recommended)

The `docker-compose.yml` automatically uses variables from `.env`:

```yaml
environment:
  USE_AWS_RDS: ${USE_AWS_RDS:-true}
  RDS_HOST: ${RDS_HOST}
  RDS_PORT: ${RDS_PORT:-5432}
  # ... more variables
```

### Via Command Line

```bash
# Pass specific variables
docker run \
  -e USE_AWS_RDS=true \
  -e RDS_HOST=your-host \
  -e RDS_PORT=5432 \
  -e RDS_USERNAME=user \
  -e RDS_PASSWORD=pass \
  -e RDS_DATABASE=postgres \
  -p 8000:8000 \
  pramith-api:latest
```

### Via .env File

Create `.env` in project root:

```env
USE_AWS_RDS=true
RDS_HOST=your-database-host
RDS_PORT=5432
RDS_DATABASE=your_db
RDS_USERNAME=your_user
RDS_PASSWORD=your_password
AWS_REGION=eu-north-1
USE_IAM_AUTH=false
```

Then run:
```bash
docker-compose up api
```

---

## 📊 Full Workflow Example

### 1. Setup

```bash
# Copy environment template
cp .env.example .env

# Edit .env with your credentials
nano .env  # or use your editor
```

### 2. Build & Start API

```bash
# Build and start in background
docker-compose up -d api

# Wait for health check
sleep 5

# Verify it's running
curl http://localhost:8000/health
```

### 3. Run Tests

```bash
# Option A: Run custom test script
docker-compose exec api python api_test_docker.py

# Option B: Run pytest in Docker
docker-compose run --rm tests

# Option C: Run specific test file
docker-compose run --rm tests pytest test_user_api.py -v
```

### 4. View Results

```bash
# Check API logs
docker-compose logs api | tail -20

# Check test output
docker-compose logs tests
```

### 5. Stop Everything

```bash
docker-compose down
```

---

## 🐛 Troubleshooting

### API Not Accessible

```bash
# Check if container is running
docker-compose ps

# View logs
docker-compose logs api

# Restart container
docker-compose restart api
```

### Database Connection Error

```bash
# Verify environment variables
docker-compose exec api env | grep RDS

# Check database connectivity
docker-compose exec api python -c "
from app.config import settings
print(f'Host: {settings.RDS_HOST}')
print(f'Database: {settings.RDS_DATABASE}')
"
```

### Port Already in Use

```bash
# Use different port
docker-compose down
docker run -p 8001:8000 pramith-api:latest
```

### Clear Everything and Start Fresh

```bash
docker-compose down -v
docker system prune -a
docker-compose up --build api
```

---

## 📋 Common Commands Reference

| Task | Command |
|------|---------|
| Build image | `docker build -t pramith-api:latest .` |
| Start API | `docker-compose up -d api` |
| Stop API | `docker-compose down` |
| View logs | `docker-compose logs -f api` |
| Run tests | `docker-compose run --rm tests` |
| Shell access | `docker-compose exec api bash` |
| Check health | `curl http://localhost:8000/health` |
| Test endpoints | `python api_test_docker.py` |
| List containers | `docker-compose ps` |
| Remove all | `docker-compose down -v` |

---

## 🎯 Testing All Endpoints

Use the provided `api_test_docker.py` script which tests:

- ✅ Health checks
- ✅ Authentication (register, login)
- ✅ User management (create, read, list)
- ✅ Doctor management (create, read, list)
- ✅ Appointments (create, read, list)
- ✅ OTP verification
- ✅ Payments

**Run it:**

```bash
docker-compose exec api python api_test_docker.py
```

---

## 📚 Additional Resources

- [Full API Documentation](./API_ENDPOINTS_WITH_EXAMPLES.md)
- [Docker Documentation](https://docs.docker.com/)
- [Docker Compose Documentation](https://docs.docker.com/compose/)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
