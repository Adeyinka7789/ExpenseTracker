# PersonalExpenseTracker
This project helps you to track your financial inflow and outflow: your income and expenses. It's an API fully written in Django Rest, Python, Redis. And it can be consumed by any front end.
💰 Personal Finance Tracker API
A secure and high-performance backend API built with Django REST Framework (DRF) for
tracking personal finances. This project demonstrates proficiency in modern backend
concepts, including secure JWT authentication, efficient data retrieval, and performance
optimization via Redis caching.
🌟 Key Features
● Secure Authentication: User registration and login protected by JSON Web Tokens
(JWT).
● CRUD for Transactions: API endpoints for logging and retrieving income and expense
transactions.
● Real-Time Analytics: Calculates and serves the user's current financial balance using a
Redis cache layer to minimize database load.
● Scalability Demo (Go): Includes a separate Go program demonstrating concurrent
processing for high-volume batch tasks, like transaction aggregation.
🚀 Getting Started
Prerequisites
1. Python 3.11+
2. Redis Server: Must be running locally (e.g., via Docker).
3. Virtual Environment (venv recommended)
1. Setup
# Clone the repository
git clone <your-repo-link>
cd finance-tracker-api/finance_tracker
# Create and activate virtual environment
python -m venv venv
# Windows:
.\venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate
# Install dependencies
pip install -r requirements.txt # Assuming you have a requirements.txt with Django, DRF, JWT,
and django-redis2. Database & Migrations
If you deleted your database (db.sqlite3) and migration files during troubleshooting, run:
# 1. Create fresh migration files
python manage.py makemigrations transactions
# 2. Apply all migrations (creates tables for User and Transaction)
python manage.py migrate
3. Run the Server
Ensure your local Redis server is running, then start the Django development server:
python manage.py runserver
The API will be available at http://127.0.0.1:8000/.
🔒 API Endpoints & Usage
All API endpoints are prefixed with /api/. Use tools like Postman, Insomnia, or cURL to interact
with the API.
Authentication Endpoints
Method Endpoint Description Requires Auth Body Response
POST /api/register/ Create a new
user account.
No username,
email,
password
Success (201)
or 400
POST /api/login/ Log in and
receive JWT
tokens.
No username,
password
access, refresh
tokens
POST /api/token/refre
sh/
Refresh
expired access
token using the
refresh token.
No refresh token New access
token
Authorization Header Format (for protected endpoints):
Authorization: Bearer YOUR_ACCESS_TOKEN
Transaction & Analytics Endpoints
Method Endpoint Description Requires Auth Body Response
POST /api/transactio
ns/
Create a new
transaction.
(Triggers Redis
Yes amount, type,
description,
category
Transaction
details (201)cache
invalidation)
GET /api/transactio
ns/
View all
transactions
for the
authenticated
user.
Yes None List of
transactions
GET /api/analytics/ Get the user's
total financial
balance.
(Served from
Redis cache)
Yes None Current
balance
Example: Creating a Transaction
Request (POST /api/transactions/)
{
"amount": 1200.00,
"type": "income",
"description": "Monthly Salary",
"category": "Work"
} ⚙️
Architectural Highlights
Custom User Model
The project uses a custom User model defined in the transactions app, allowing for future
expansion beyond the standard Django user fields.
Redis Caching for Analytics
The /api/analytics/ endpoint implements a critical caching layer:
1. Read: On a GET request, the view first checks Redis for the user's balance.
2. Cache Hit: If found, the cached balance is returned immediately (<50ms).
3. Cache Miss: If not found, the balance is computed by aggregating transactions from
the database, and the result is stored in Redis for future requests (e.g., with a 5-minute
TTL).
4. Invalidation: Upon POST (new transaction), the associated user's balance cache key is
cleared, ensuring the next analytics request computes a fresh balance.
⚡ Go Concurrency Demo
A simple, standalone Go program is included to demonstrate the concept of parallelprocessing for large-scale financial data aggregation.
This is analogous to a scenario where high-volume transaction monitoring or batch analytics
requires efficient, non-blocking I/O, a common requirement in fintech backends.
Running the Go Demo
1. Ensure Go is installed on your system.
2. Navigate to the directory containing the Go file (e.g., go_batch_processor/main.go).
3. Execute the program:
go run main.go
(The output demonstrates that aggregation is handled concurrently using goroutines
and wait groups.)
