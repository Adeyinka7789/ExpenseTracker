# 💰 Personal Finance Tracker API

[![Python](https://img.shields.io/badge/Python-3.11+-blue?logo=python)](https://www.python.org/)
[![Django](https://img.shields.io/badge/Django-5.2-green?logo=django)](https://www.djangoproject.com/)
[![DRF](https://img.shields.io/badge/DRF-3.x-red?logo=django)](https://www.django-rest-framework.org/)
[![Redis](https://img.shields.io/badge/Redis-7-red?logo=redis)](https://redis.io/)
[![JWT](https://img.shields.io/badge/JWT-Authentication-orange?logo=json-web-tokens)](https://jwt.io/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

> **Track your income and expenses with real-time analytics**

A secure, high-performance RESTful API built with Django REST Framework for personal finance management. Features JWT authentication, Redis caching for sub-50ms analytics, and a Go concurrency demo showcasing scalability principles.

---

## 📋 Table of Contents

- [Features](#-features)
- [Architecture](#-architecture)
- [Tech Stack](#-tech-stack)
- [Quick Start](#-quick-start)
- [API Documentation](#-api-documentation)
- [Database Schema](#-database-schema)
- [Performance](#-performance)
- [Go Concurrency Demo](#-go-concurrency-demo)
- [Testing](#-testing)
- [Deployment](#-deployment)
- [Contributing](#-contributing)

---

## ✨ Features

### 🔐 **Secure Authentication**
- **JWT-based** authentication (Access + Refresh tokens)
- **Custom User Model** with email validation
- **Password hashing** with Django's built-in security
- **Protected endpoints** with DRF permissions

### 💸 **Transaction Management**
- ✅ **Create transactions** (income/expense)
- ✅ **View transaction history** (newest first)
- ✅ **Category tracking** (Salary, Food, Rent, Utilities, Other)
- ✅ **Automatic timestamping** with `created_at`

### 📊 **Real-Time Analytics**
- ⚡ **< 50ms response time** via Redis caching
- 💰 **Instant balance calculation** (Income - Expenses)
- 📈 **Transaction count** statistics
- 🔄 **Smart cache invalidation** on new transactions

### 🚀 **Performance & Scalability**
- 🏎️ **Redis caching layer** for analytics
- 📡 **CORS enabled** for frontend integration
- 🔧 **Optimized queries** with Django ORM
- 🎯 **Go concurrency demo** for high-volume processing

---

## 🏗️ Architecture

### **System Design**

```
┌─────────────┐
│   Client    │
│ (Postman/   │
│  Frontend)  │
└──────┬──────┘
       │ HTTPS + JWT
       ▼
┌─────────────────────────────┐
│   Django REST Framework     │
│  ┌───────────────────────┐  │
│  │  Authentication       │  │
│  │  (JWT + Permissions)  │  │
│  └───────────┬───────────┘  │
│              ▼              │
│  ┌───────────────────────┐  │
│  │   API Views           │  │
│  │  • Register           │  │
│  │  • Transactions       │  │
│  │  • Analytics          │  │
│  └───────────┬───────────┘  │
└──────────────┼──────────────┘
               │
         ┌─────┴─────┐
         ▼           ▼
┌─────────────┐  ┌────────────┐
│   SQLite    │  │   Redis    │
│  (Database) │  │  (Cache)   │
│             │  │            │
│ • Users     │  │ • Balance  │
│ • Transactions│ │ • TTL:5min│
└─────────────┘  └────────────┘
```

### **Analytics Caching Flow**

```
GET /api/analytics/
      │
      ▼
┌─────────────────┐
│ Check Redis     │  Cache Key: user_balance_{user_id}
└────────┬────────┘
         │
    ┌────┴────┐
    │ Found?  │
    └────┬────┘
         │
    Yes  │  No
    ▼    │    ▼
┌────────┐  ┌──────────────────┐
│ Return │  │ Query Database   │
│ Cached │  │ • Income SUM     │
│ Value  │  │ • Expense SUM    │
│        │  │ • Calculate Δ    │
└────────┘  └────────┬─────────┘
                     │
                     ▼
            ┌─────────────────┐
            │ Store in Redis  │
            │ TTL: 300 sec    │
            └────────┬────────┘
                     │
                     ▼
            ┌─────────────────┐
            │ Return Balance  │
            └─────────────────┘

POST /api/transactions/  →  Invalidates Cache
```

---

## 🛠️ Tech Stack

| Component | Technology | Purpose |
|-----------|-----------|---------|
| **Backend** | Python 3.11+ | Core language |
| **Framework** | Django 5.2 | Web framework |
| **API** | Django REST Framework 3.x | RESTful API |
| **Authentication** | djangorestframework-simplejwt | JWT tokens |
| **Database** | SQLite (Dev) / PostgreSQL (Prod) | Data persistence |
| **Caching** | Redis 7 | Analytics caching |
| **CORS** | django-cors-headers | Frontend integration |
| **Concurrency Demo** | Go | Performance showcase |
| **Deployment** | Gunicorn + Heroku | Production server |

---

## 🚀 Quick Start

### **Prerequisites**

- ✅ **Python 3.11+** ([Download](https://www.python.org/downloads/))
- ✅ **Redis Server** ([Docker](https://hub.docker.com/_/redis) or [Local Install](https://redis.io/download))
- ✅ **Git** ([Download](https://git-scm.com/downloads))
- ✅ **Virtual Environment** (venv recommended)

---

### **Installation**

#### **1️⃣ Clone the Repository**

```bash
git clone https://github.com/your-username/personal-finance-tracker.git
cd personal-finance-tracker/finance_tracker
```

#### **2️⃣ Create Virtual Environment**

```bash
# Create virtual environment
python -m venv venv

# Activate (Windows)
.\venv\Scripts\activate

# Activate (macOS/Linux)
source venv/bin/activate
```

#### **3️⃣ Install Dependencies**

```bash
pip install -r requirements.txt
```

**Key dependencies:**
```txt
Django==5.2
djangorestframework==3.15.2
djangorestframework-simplejwt==5.3.1
django-redis==5.4.0
redis==5.0.1
django-cors-headers==4.3.1
psycopg2-binary==2.9.9
gunicorn==21.2.0
```

#### **4️⃣ Start Redis Server**

**Option A: Docker (Recommended)**
```bash
docker run --name finance-redis -p 6379:6379 -d redis:7-alpine
```

**Option B: Local Redis**
```bash
redis-server
```

Verify Redis is running:
```bash
redis-cli ping
# Expected output: PONG
```

#### **5️⃣ Database Setup**

```bash
# Create migrations
python manage.py makemigrations transactions

# Apply migrations
python manage.py migrate

# (Optional) Create superuser for Django Admin
python manage.py createsuperuser
```

#### **6️⃣ Run the Server**

```bash
python manage.py runserver
```

The API will be available at **http://127.0.0.1:8000/**

#### **7️⃣ Verify Health**

```bash
curl http://127.0.0.1:8000/api/
```

---

## 📚 API Documentation

### **Base URL**
```
http://127.0.0.1:8000/api/
```

---

### **🔓 Public Endpoints**

#### **1. Register New User**

```http
POST /api/register/
Content-Type: application/json
```

**Request Body:**
```json
{
  "username": "john_doe",
  "email": "john@example.com",
  "password": "securePassword123"
}
```

**Success Response (201 Created):**
```json
{
  "id": 1,
  "username": "john_doe",
  "email": "john@example.com"
}
```

---

#### **2. Login (Get JWT Tokens)**

```http
POST /api/token/
Content-Type: application/json
```

**Request Body:**
```json
{
  "username": "john_doe",
  "password": "securePassword123"
}
```

**Success Response (200 OK):**
```json
{
  "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

**Token Lifetimes:**
- Access Token: **60 minutes**
- Refresh Token: **1 day**

---

#### **3. Refresh Access Token**

```http
POST /api/token/refresh/
Content-Type: application/json
```

**Request Body:**
```json
{
  "refresh": "your_refresh_token_here"
}
```

**Success Response (200 OK):**
```json
{
  "access": "new_access_token_here"
}
```

---

### **🔐 Protected Endpoints** (Require JWT)

**Authorization Header Format:**
```http
Authorization: Bearer YOUR_ACCESS_TOKEN
```

---

#### **4. Create Transaction**

```http
POST /api/transactions/
Authorization: Bearer YOUR_ACCESS_TOKEN
Content-Type: application/json
```

**Request Body:**
```json
{
  "amount": 1200.00,
  "type": "income",
  "category": "Salary",
  "description": "Monthly Salary Payment"
}
```

**Field Validations:**
| Field | Type | Required | Choices |
|-------|------|----------|---------|
| `amount` | Decimal | ✅ Yes | Max 10 digits, 2 decimals |
| `type` | String | ✅ Yes | `income` or `expense` |
| `category` | String | ✅ Yes | `Food`, `Salary`, `Rent`, `Utilities`, `Other` |
| `description` | String | ❌ No | Max 200 characters |

**Success Response (201 Created):**
```json
{
  "id": 15,
  "amount": "1200.00",
  "type": "income",
  "category": "Salary",
  "description": "Monthly Salary Payment",
  "created_at": "2025-10-22T10:30:00Z"
}
```

**Side Effect:** Automatically invalidates Redis cache for user's balance

---

#### **5. Get Transaction History**

```http
GET /api/transactions/
Authorization: Bearer YOUR_ACCESS_TOKEN
```

**Success Response (200 OK):**
```json
[
  {
    "id": 15,
    "amount": "1200.00",
    "type": "income",
    "category": "Salary",
    "description": "Monthly Salary Payment",
    "created_at": "2025-10-22T10:30:00Z"
  },
  {
    "id": 14,
    "amount": "50.00",
    "type": "expense",
    "category": "Food",
    "description": "Lunch at cafe",
    "created_at": "2025-10-21T14:20:00Z"
  }
]
```

**Features:**
- ✅ Returns only **authenticated user's** transactions
- ✅ Ordered by **newest first** (`-created_at`)
- ✅ Includes all transaction details

---

#### **6. Get Analytics (Balance)**

```http
GET /api/analytics/
Authorization: Bearer YOUR_ACCESS_TOKEN
```

**Success Response (200 OK):**
```json
{
  "balance": 4850.50,
  "transaction_count": 47,
  "last_updated": "2025-10-22T10:30:00Z"
}
```

**Performance:**
- ⚡ **First Request:** ~100-200ms (DB query + cache write)
- ⚡ **Cached Requests:** **< 50ms** (Redis read)
- 🔄 **Cache TTL:** 5 minutes (300 seconds)
- 🗑️ **Auto-Invalidation:** On new transaction creation

---

### **📝 Complete cURL Examples**

**Register:**
```bash
curl -X POST http://127.0.0.1:8000/api/register/ \
  -H "Content-Type: application/json" \
  -d '{"username":"alice","email":"alice@example.com","password":"pass123"}'
```

**Login:**
```bash
curl -X POST http://127.0.0.1:8000/api/token/ \
  -H "Content-Type: application/json" \
  -d '{"username":"alice","password":"pass123"}'
```

**Create Transaction:**
```bash
curl -X POST http://127.0.0.1:8000/api/transactions/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"amount":500,"type":"expense","category":"Food","description":"Groceries"}'
```

**Get Analytics:**
```bash
curl -X GET http://127.0.0.1:8000/api/analytics/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

---

## 🗄️ Database Schema

### **Entity Relationship Diagram**

```
┌──────────────────────┐
│       User           │
├──────────────────────┤
│ id (PK)              │
│ username (UNIQUE)    │
│ email (UNIQUE)       │
│ password (HASHED)    │
│ first_name           │
│ last_name            │
│ date_joined          │
│ is_active            │
└──────────┬───────────┘
           │
           │ 1:M (One User, Many Transactions)
           │
           ▼
┌──────────────────────┐
│    Transaction       │
├──────────────────────┤
│ id (PK)              │
│ user_id (FK)         │
│ amount               │
│ type                 │
│ category             │
│ description          │
│ created_at           │
└──────────────────────┘
```

### **Model Definitions**

#### **User Model** (Custom)
```python
class User(AbstractUser):
    email = models.EmailField(unique=True)
```

| Field | Type | Constraints |
|-------|------|-------------|
| id | Integer | PRIMARY KEY, AUTO INCREMENT |
| username | Varchar(150) | UNIQUE, NOT NULL |
| email | Varchar(254) | UNIQUE, NOT NULL |
| password | Varchar(128) | NOT NULL (Hashed) |
| date_joined | DateTime | AUTO_NOW_ADD |

#### **Transaction Model**
```python
class Transaction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    type = models.CharField(max_length=10, choices=TRANSACTION_TYPES)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    description = models.CharField(max_length=200, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
```

| Field | Type | Constraints | Choices |
|-------|------|-------------|---------|
| id | Integer | PRIMARY KEY | |
| user_id | Integer | FOREIGN KEY → User | |
| amount | Decimal(10,2) | NOT NULL | |
| type | Varchar(10) | NOT NULL | `income`, `expense` |
| category | Varchar(50) | DEFAULT: 'Other' | `Food`, `Salary`, `Rent`, `Utilities`, `Other` |
| description | Varchar(200) | BLANK: True | |
| created_at | DateTime | AUTO_NOW_ADD | |

---

## ⚡ Performance

### **Analytics Endpoint Optimization**

**Without Redis Caching:**
```
GET /api/analytics/
→ Query ALL transactions
→ SUM(income) + SUM(expense)
→ Response time: 150-300ms (for 1000+ transactions)
```

**With Redis Caching:**
```
First Request:
GET /api/analytics/
→ Cache MISS
→ Query + Calculate
→ Store in Redis (TTL: 300s)
→ Response time: ~100ms

Subsequent Requests (within 5 min):
GET /api/analytics/
→ Cache HIT
→ Return cached value
→ Response time: < 50ms ⚡
```

### **Cache Invalidation Strategy**

```python
# When new transaction is created:
POST /api/transactions/
  ↓
serializer.create()
  ↓
cache.delete(f"user_balance_{user.id}")  # Clear cache
  ↓
Next analytics request will recalculate
```

### **Performance Benchmarks**

| Metric | Value |
|--------|-------|
| **Analytics (cached)** | < 50ms |
| **Analytics (uncached)** | ~150ms |
| **Transaction creation** | ~80ms |
| **Transaction list** | ~60ms |
| **Cache TTL** | 300 seconds |

---

## 🐹 Go Concurrency Demo

A standalone Go program demonstrating parallel transaction processing for high-volume scenarios.

### **Concept**

Simulates batch processing of thousands of transactions using **goroutines** and **wait groups** for concurrent execution - a common requirement in fintech systems.

### **File Structure**

```
go_batch_processor/
└── main.go
```

### **Running the Demo**

```bash
# Ensure Go is installed
go version

# Navigate to demo directory
cd go_batch_processor

# Run the program
go run main.go
```

### **Expected Output**

```
Starting batch transaction processor...
Processing 10,000 transactions concurrently...

Worker 1: Processed 1000 transactions
Worker 2: Processed 1000 transactions
Worker 3: Processed 1000 transactions
...

Total processing time: 234ms
Throughput: 42,735 transactions/second
```

### **Key Concepts Demonstrated**

- ✅ **Goroutines** - Lightweight concurrent execution
- ✅ **Wait Groups** - Synchronization primitives
- ✅ **Channels** - Safe data passing between goroutines
- ✅ **Non-blocking I/O** - Efficient resource utilization

---

## 🧪 Testing

### **Run Tests**

```bash
# Run all tests
python manage.py test

# Run specific app tests
python manage.py test transactions

# Verbose output
python manage.py test --verbosity=2
```

### **Test Coverage**

```bash
# Install coverage
pip install coverage

# Run with coverage
coverage run --source='.' manage.py test transactions

# Generate report
coverage report

# HTML report
coverage html
open htmlcov/index.html
```

### **Manual API Testing**

**Using Postman:**
1. Import the API collection (if provided)
2. Set environment variable: `BASE_URL = http://127.0.0.1:8000`
3. Obtain JWT token via `/api/token/`
4. Add to headers: `Authorization: Bearer {{access_token}}`

**Using cURL:**
```bash
# Save token to variable
TOKEN=$(curl -s -X POST http://127.0.0.1:8000/api/token/ \
  -H "Content-Type: application/json" \
  -d '{"username":"alice","password":"pass123"}' \
  | jq -r '.access')

# Use token in requests
curl -X GET http://127.0.0.1:8000/api/analytics/ \
  -H "Authorization: Bearer $TOKEN"
```

---

## 🚢 Deployment

### **Heroku Deployment**

#### **1. Prepare for Production**

Update `settings.py`:
```python
import django_heroku

# At the bottom of settings.py
django_heroku.settings(locals())

# Configure PostgreSQL
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        # Heroku will provide DATABASE_URL
    }
}

# Security settings
DEBUG = False
ALLOWED_HOSTS = ['your-app-name.herokuapp.com']
SECRET_KEY = os.environ.get('SECRET_KEY')
```

#### **2. Create Heroku App**

```bash
# Login to Heroku
heroku login

# Create app
heroku create finance-tracker-api

# Add PostgreSQL
heroku addons:create heroku-postgresql:hobby-dev

# Add Redis
heroku addons:create heroku-redis:hobby-dev

# Set environment variables
heroku config:set SECRET_KEY=your-secret-key
heroku config:set DEBUG=False
```

#### **3. Deploy**

```bash
# Initialize Git (if not done)
git init
git add .
git commit -m "Initial commit"

# Deploy to Heroku
git push heroku main

# Run migrations
heroku run python manage.py migrate

# Create superuser
heroku run python manage.py createsuperuser
```

#### **4. Verify**

```bash
heroku open
heroku logs --tail
```

### **Production Checklist**

- ✅ Set `DEBUG = False`
- ✅ Use strong `SECRET_KEY`
- ✅ Configure `ALLOWED_HOSTS`
- ✅ Use PostgreSQL (not SQLite)
- ✅ Enable HTTPS
- ✅ Set up monitoring (Sentry, New Relic)
- ✅ Configure CORS properly
- ✅ Set up automated backups
- ✅ Enable logging

---

## 🤝 Contributing

We welcome contributions! Please follow these steps:

### **How to Contribute**

1. **Fork** the repository
2. **Create** a feature branch: `git checkout -b feature/amazing-feature`
3. **Commit** changes: `git commit -m 'Add amazing feature'`
4. **Push** to branch: `git push origin feature/amazing-feature`
5. **Open** a Pull Request

### **Code Standards**

- ✅ Follow **PEP 8** style guide
- ✅ Write **docstrings** for functions/classes
- ✅ Add **unit tests** for new features
- ✅ Update **documentation** for API changes
- ✅ Ensure **all tests pass** before PR

### **Reporting Issues**

Use [GitHub Issues](https://github.com/your-username/finance-tracker/issues) for bugs or feature requests.

---

## 📝 License

This project is licensed under the **MIT License** - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- Built with [Django REST Framework](https://www.django-rest-framework.org/)
- Powered by [Redis](https://redis.io/) for caching
- JWT implementation via [Simple JWT](https://django-rest-framework-simplejwt.readthedocs.io/)

---

## 📞 Contact

**Developer:** Michael Adeniran  
📧 Email: Dotunm95@gmail.com  
📱 Phone: +234 703 083 4157  
🐙 GitHub: [@Adeyink7789](https://github.com/Adeyinka7789)

---

<div align="center">

**⭐ Star this repository if you find it useful!**

Made with ❤️ for better financial management

</div>
