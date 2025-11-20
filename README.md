# Financial Dashboard 🚀

**Your Personal Financial Control Panel - Like a Car Dashboard for Your Money!**

> *Track currencies, stocks, and cryptocurrencies in one place with real-time updates and beautiful visualizations*

## 🎯 What is Financial Dashboard?

Imagine your car's dashboard - you see speed, fuel level, engine temperature. **Financial Dashboard** shows similar "instruments" but for your finances:

- **Currency Rates** 📈
- **Stock Prices** 📊  
- **Cryptocurrencies** ₿
- **Change Graphs** 📉

### 🛠 How It Works Technically?

**Think of our dashboard as a financial "aggregator":**

1. **Data Collection** - Like a postman collecting mail from different post offices:
   - Goes to Central Bank of Russia → gets currency rates
   - Goes to Moscow Exchange → gets stock quotes  
   - Goes to Binance → gets cryptocurrency data

2. **Data Processing** - Like a secretary sorting mail:
   - Validates data for correctness
   - Saves to database (like an archive)
   - Caches (puts copies in fast access)

3. **Display** - Like a dispatcher showing information on screen:
   - Beautiful cards with numbers
   - Color indicators (green - growth, red - decline)
   - Change graphs over time

4. **Real-time Updates** - Like live broadcast:
   - Data updates automatically every 30 seconds
   - No manual page refresh needed
   - All changes visible instantly

## 📊 What Users See?

**Simple and intuitive interface:**

```
💵 CURRENCIES (Central Bank of Russia)
USD/RUB: 89.50 ₽ ↗ +0.15
EUR/RUB: 97.80 ₽ ↗ +0.20

📈 STOCKS (Moscow Exchange)
SBER: 280.50 ₽ ↗ +1.2%
GAZP: 165.30 ₽ ↘ -0.5%

₿ CRYPTOCURRENCIES (Binance)
BTC/RUB: 3,450,000 ↗ +2.1%
ETH/RUB: 225,000 ↗ +1.8%
```

## 🚀 Why This is Convenient?

### Before you had to:
- Open 3-5 different websites
- Memorize or write down numbers  
- Compare manually
- Constantly refresh pages

### Now:
- **One window** - all data in one place
- **Automatic updates** - no need to refresh anything
- **Change history** - see trends on graphs
- **Notifications** - system warns about important changes

## 🌟 What Makes Our Approach Unique?

We created not just "another rates website", but a **full-fledged platform** that:

- **Collects data from reliable sources** (CBR, MOEX, Binance)
- **Works in real-time** without delays
- **Saves history** for trend analysis
- **Beautifully displays** complex information in simple way
- **Ready to work 24/7** with monitoring system

## 💡 Simple Analogy

**Financial Dashboard is like "Yandex.Weather" for finances:**

- Shows current "weather" in markets
- Gives forecast based on historical data
- Collects information from different "weather stations"
- Updates automatically
- Shows everything in simple and beautiful interface

Now you can track "financial weather" as easily as regular weather outside! ☀️📈

---

# 🏗 Project Implementation Status

## ✅ **COMPLETED - Phase 1 & 2**

### 🎯 Phase 1: Project Foundation & CBR API
**Status:** ✅ **FULLY IMPLEMENTED**

**What we built:**
- Production-ready FastAPI application with proper structure
- CBR (Central Bank of Russia) service with intelligent caching
- Professional development environment with Poetry and linters
- Comprehensive testing with async support
- Auto-generated API documentation

**Technical Achievements:**
- ✅ FastAPI with async/await support
- ✅ Pydantic models with validation
- ✅ Error handling and structured logging
- ✅ Code quality tools (Black, Flake8, MyPy, Pytest)
- ✅ REST API with Swagger/ReDoc documentation

### 🎯 Phase 2: MOEX API & Database
**Status:** ✅ **FULLY IMPLEMENTED**

**What we built:**
- PostgreSQL database with Docker Compose
- SQLAlchemy ORM models for financial data
- MOEX (Moscow Exchange) service with complex JSON parsing
- Alembic database migrations
- Extended API endpoints for stocks

**Technical Achievements:**
- ✅ PostgreSQL with health checks and persistence
- ✅ SQLAlchemy 2.0 with async support
- ✅ MOEX API integration with error handling
- ✅ Database migrations with Alembic
- ✅ Professional project structure

## 🚧 **UPCOMING PHASES**

### 🎯 Phase 3: Redis Caching & Binance API
**Status:** 🔄 **PLANNED**

**What we'll build:**
- Redis caching for performance optimization
- Binance API integration for cryptocurrencies
- Cache strategies with TTL and error handling
- Unified interface for all financial services

### 🎯 Phase 4: WebSockets & Real-time Updates
**Status:** 🔄 **PLANNED**

**What we'll build:**
- WebSocket connections for real-time data
- Connection manager with broadcast functionality
- Data aggregator for all sources
- Heartbeat mechanisms for connection health

### 🎯 Phase 5: Dash Dashboard & Visualization
**Status:** 🔄 **PLANNED**

**What we'll build:**
- Interactive Dash/Plotly dashboard
- Real-time data visualization
- Beautiful UI with CSS styling
- Automatic updates every 30 seconds

### 🎯 Phase 6: Background Tasks & Historical Data
**Status:** 🔄 **PLANNED**

**What we'll build:**
- Celery for background tasks
- Historical data storage
- Price alert system
- Scheduled tasks with Celery Beat

### 🎯 Phase 7: Production Deployment & Monitoring
**Status:** 🔄 **PLANNED**

**What we'll build:**
- Docker production setup
- Cloud deployment (Railway/Render)
- Prometheus monitoring and metrics
- Health checks and logging

---

# 🛠 Technical Implementation

## 📁 Project Structure

```
financial_dashboard/
├── app/                          # Main application
│   ├── api/                      # API routes
│   │   ├── __init__.py
│   │   └── endpoints.py          # REST API endpoints
│   ├── core/                     # Core configuration
│   │   ├── __init__.py
│   │   └── config.py             # App settings
│   ├── services/                 # External API services
│   │   ├── __init__.py
│   │   ├── cbr_service.py        # Central Bank Russia
│   │   └── moex_service.py       # Moscow Exchange
│   ├── models/                   # Database models
│   │   ├── __init__.py
│   │   └── financial_models.py   # SQLAlchemy models
│   ├── db/                       # Database configuration
│   │   ├── __init__.py
│   │   └── session.py            # DB sessions
│   └── main.py                   # FastAPI app
├── alembic/                      # Database migrations
│   ├── versions/                 # Migration scripts
│   └── env.py                    # Migration config
├── tests/                        # Test suite
│   ├── test_cbr.py               # CBR tests
│   └── test_moex.py              # MOEX tests
├── docker-compose.yml            # Docker services
├── pyproject.toml                # Dependencies
└── README.md                     # Documentation
```

## 🚀 Quick Start

### Prerequisites
- **Python 3.12+**
- **Poetry** (dependency management)
- **Docker & Docker Compose** (for database)

### Installation & Setup

1. **Clone and setup:**
```bash
git clone <repository-url>
cd financial_dashboard
```

2. **Install dependencies:**
```bash
poetry install --no-root
```

3. **Setup environment:**
```bash
cp .env.example .env
# Edit .env if needed
```

4. **Start database:**
```bash
docker-compose up -d postgres
```

5. **Run migrations:**
```bash
poetry run alembic upgrade head
```

6. **Start development server:**
```bash
poetry run uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

7. **Access the application:**
   - **API**: http://localhost:8000
   - **Documentation**: http://localhost:8000/docs
   - **Database Admin**: http://localhost:8080 (email: `admin@financial.com`, password: `admin`)

## 📊 API Endpoints

### Core Endpoints
- `GET /` - API information
- `GET /health` - Health check with database status

### Currency Data (CBR)
- `GET /api/v1/rates/cbr` - All currency rates
- `GET /api/v1/rates/cbr/{currency}` - Specific currency (USD, EUR, CNY, GBP, JPY)
- `GET /api/v1/currencies/supported` - Supported currencies

### Stock Data (MOEX)
- `GET /api/v1/stocks/moex` - All stock prices
- `GET /api/v1/stocks/moex/{ticker}` - Specific stock (SBER, GAZP, VTBR, etc.)
- `GET /api/v1/stocks/supported` - Supported stocks

### Example Usage
```bash
# Get all currency rates
curl http://localhost:8000/api/v1/rates/cbr

# Get USD rate
curl http://localhost:8000/api/v1/rates/cbr/USD

# Get all stocks
curl http://localhost:8000/api/v1/stocks/moex

# Get SBER stock
curl http://localhost:8000/api/v1/stocks/moex/SBER
```

## 🛠 Development

### Code Quality
```bash
# Format code
poetry run black app tests
poetry run isort app tests

# Lint and type check
poetry run flake8 app tests
poetry run mypy app

# Run tests
poetry run pytest
poetry run pytest --cov=app --cov-report=html

# Full quality check
poetry run black --check app tests && \
poetry run flake8 app tests && \
poetry run mypy app && \
poetry run pytest
```

### Database Operations
```bash
# Create migration
poetry run alembic revision --autogenerate -m "description"

# Apply migrations
poetry run alembic upgrade head

# Check status
poetry run alembic current
```

## 🎯 Learning Journey

### Skills You're Building:

**Phase 1-2 (Completed):**
- ✅ Production-ready FastAPI applications
- ✅ Async programming with aiohttp
- ✅ SQLAlchemy ORM and database design
- ✅ Docker Compose for service orchestration
- ✅ External API integrations (CBR, MOEX)
- ✅ Professional testing strategies
- ✅ Code quality and best practices

**Upcoming Phases:**
- Redis caching and performance optimization
- WebSockets for real-time communication
- Data visualization with Dash/Plotly
- Background tasks with Celery
- Production deployment and monitoring
- Full-stack application development

## 🏆 Resume-Worthy Achievements

```markdown
## Financial Dashboard - Full-stack Python Application

**Current Implementation:**
- Developed FastAPI backend with async/await support
- Integrated Central Bank Russia and Moscow Exchange APIs
- Implemented PostgreSQL database with SQLAlchemy ORM
- Set up Docker Compose with health checks and persistence
- Created comprehensive test suite with 80%+ coverage
- Configured professional development environment

**Technical Stack:**
- Backend: FastAPI, SQLAlchemy, Pydantic, Alembic
- Database: PostgreSQL, Asyncpg
- APIs: CBR (currency rates), MOEX (stock prices)
- Infrastructure: Docker, Docker Compose
- Quality: Pytest, Black, Flake8, MyPy
- Documentation: Auto-generated Swagger/ReDoc

**Key Features:**
- Real-time financial data aggregation
- Robust error handling and caching
- Database migrations and version control
- REST API with comprehensive documentation
- Production-ready architecture
```

## 🤝 Contributing

We welcome contributions! Here's how you can help:

1. **Report bugs** - Open an issue with detailed description
2. **Suggest features** - Share your ideas for improvement
3. **Submit pull requests** - Follow our development standards

### Development Standards
```bash
# Before submitting PR, ensure all checks pass:
poetry run black app tests
poetry run flake8 app tests  
poetry run mypy app
poetry run pytest --cov=app --cov-fail-under=80
```

## 📄 License

This project is licensed under the MIT License - see details in LICENSE file.

## 👥 Author

- **Roman Geller** - [roma.geller@mail.ru](mailto:roma.geller@mail.ru)

## 🙏 Acknowledgments

- **Central Bank of Russia** for currency rate API
- **Moscow Exchange** for stock market data
- **FastAPI** team for excellent web framework
- **Python community** for amazing development tools
- **Docker** team for containerization platform

---

**🚀 Ready to track your financial weather? Start using Financial Dashboard today!**


*Note: This is an educational project. Always verify financial data with official sources before making investment decisions.*
