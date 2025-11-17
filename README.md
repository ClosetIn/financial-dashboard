# Financial Dashboard

Real-time financial data dashboard with FastAPI, providing currency rates from Central Bank of Russia with intelligent caching and error handling.

## Features

- Real-time currency rates from Central Bank of Russia (USD, EUR, CNY, GBP, JPY)
- FastAPI with full async/await support
- Type hints with Pydantic models and validation
- Comprehensive testing with pytest and async support
- Code quality tools (Black, Flake8, MyPy, Pylint, pytest-cov)
- Auto-generated API documentation (Swagger UI & ReDoc)
- Intelligent caching with fallback to cached data on API errors
- Robust error handling and structured logging
- Environment-based configuration with pydantic-settings

## Tech Stack

- Python 3.12+
- FastAPI - Modern, fast web framework for building APIs
- Poetry - Dependency management and packaging
- Pydantic v2 - Data validation with field_validator
- aiohttp - Async HTTP client for API requests
- Uvicorn - ASGI server
- pytest - Testing framework with asyncio support

## Project Structure

```
financial_dashboard/
├── app/
│   ├── api/
│   │   ├── __init__.py
│   │   └── endpoints.py
│   ├── core/
│   │   ├── __init__.py
│   │   └── config.py
│   ├── services/
│   │   ├── __init__.py
│   │   └── cbr_service.py
│   ├── models/
│   │   ├── __init__.py
│   │   └── financial_models.py
│   └── main.py
├── tests/
│   ├── __init__.py
│   └── test_cbr.py
├── dashboard/
├── pyproject.toml
├── .flake8
├── .env.example
└── README.md
```

## Quick Start

### Prerequisites

- Python 3.12 or higher
- Poetry 2.2.1 or higher

### Installation & Setup

1. Clone and setup the project:
```bash
git clone <repository-url>
cd financial_dashboard
```

2. Install dependencies with Poetry:
```bash
poetry install
```

3. Setup environment configuration:
```bash
cp .env.example .env
```

4. Activate virtual environment:
```bash
poetry env activate
```

5. Start the development server:
```bash
poetry run uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

6. Access the application:
- API: http://localhost:8000
- Interactive Documentation: http://localhost:8000/docs
- Alternative Documentation: http://localhost:8000/redoc

## API Endpoints

### Core Endpoints
- `GET /` - Root endpoint with API information
- `GET /health` - Health check and service status monitoring

### Financial Data Endpoints
- `GET /api/v1/rates/cbr` - Get all CBR currency rates with change metrics
- `GET /api/v1/rates/cbr/{currency}` - Get specific currency rate (USD, EUR, CNY, GBP, JPY)
- `GET /api/v1/currencies/supported` - List of supported currencies

### Example Usage

```bash
# Get all currency rates with change data
curl http://localhost:8000/api/v1/rates/cbr

# Get specific currency rate (USD)
curl http://localhost:8000/api/v1/rates/cbr/USD

# Get list of supported currencies
curl http://localhost:8000/api/v1/currencies/supported
```

### Response Format
```json
{
  "source": "cbr",
  "data": {
    "USD": {
      "currency": "USD/RUB",
      "rate": 91.5,
      "change": 0.2,
      "change_percent": 0.22,
      "timestamp": "2024-01-18T01:07:11.786"
    }
  },
  "timestamp": "2024-01-18T01:07:11.786",
  "currencies_count": 5,
  "success": true
}
```

## Development

### Code Quality & Testing Commands

**Formatting and Linting:**
```bash
# Format code with Black
poetry run black app tests

# Sort imports with isort
poetry run isort app tests

# Check code style with Flake8
poetry run flake8 app tests

# Static type checking with MyPy
poetry run mypy app
```

**Testing:**
```bash
# Run all tests
poetry run pytest

# Run tests with verbose output
poetry run pytest -v

# Run tests with coverage report in console
poetry run pytest --cov=app --cov-report=term-missing

# Generate HTML coverage report
poetry run pytest --cov=app --cov-report=html
```

**Full Quality Check (CI/CD ready):**
```bash
poetry run black --check app tests && \
poetry run flake8 app tests && \
poetry run mypy app && \
poetry run pytest
```

### Running Modes

**Development (with auto-reload):**
```bash
poetry run uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

**Production:**
```bash
poetry run uvicorn app.main:app --host 0.0.0.0 --port 8000
```

## Testing Strategy

The project includes comprehensive tests covering:

- CBRService integration with mock API responses
- CurrencyRate model validation and business logic
- Error handling for network failures and invalid data
- Async operations with pytest-asyncio
- Edge cases like negative values and missing currencies

Run the test suite:
```bash
poetry run pytest
```

## Configuration

Configuration is managed through environment variables. Create a `.env` file based on `.env.example`:

```env
# Basic settings
DEBUG=true
PROJECT_NAME="Financial Dashboard"

# Server settings
HOST=0.0.0.0
PORT=8000

# CORS settings (as JSON string)
CORS_ORIGINS='["*"]'
```

## CBR API Integration

The application integrates with the Central Bank of Russia's JSON API:

- **Endpoint**: `https://www.cbr-xml-daily.ru/daily_json.js`
- **Data Format**: JSON with daily currency rates
- **Features**:
  - Real-time rate fetching with HTTP headers
  - Change calculation (absolute and percentage)
  - Intelligent caching to respect API limits
  - Graceful fallback to cached data on network errors
  - Comprehensive error handling and logging

### Supported Currencies
- USD - US Dollar
- EUR - Euro
- CNY - Chinese Yuan
- GBP - British Pound
- JPY - Japanese Yen

## Implementation Details

### Key Components

**CBRService** (`app/services/cbr_service.py`):
- Async context manager for HTTP sessions
- JSON parsing with error handling
- Intelligent caching mechanism
- Currency change calculations

**CurrencyRate Model** (`app/services/cbr_service.py`):
- Pydantic v2 with field_validator
- Automatic value rounding and validation
- Timestamp tracking

**FastAPI Application** (`app/main.py`):
- Application factory pattern
- CORS middleware configuration
- Structured logging setup
- Health check endpoints

## Future Enhancements

### Phase 2: Database & Advanced Features
- PostgreSQL database integration
- SQLAlchemy ORM models for historical data
- MOEX (Moscow Exchange) API integration
- Alembic database migrations
- WebSocket real-time updates

### Phase 3: Production Ready
- Docker containerization
- Frontend dashboard with charts
- User authentication and authorization
- Rate limiting and API throttling
- CI/CD pipeline with GitHub Actions

## Code Quality Standards

This project maintains high code quality through:

- Black: Consistent code formatting (88 char line length)
- Flake8: Python style guide enforcement (configured for Black compatibility)
- MyPy: Static type checking with strict settings
- Pytest: Comprehensive test coverage with async support
- Pylint: Additional code analysis

## Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/amazing-feature`
3. Make your changes and ensure all checks pass:
```bash
poetry run black app tests && \
poetry run flake8 app tests && \
poetry run mypy app && \
poetry run pytest
```
4. Commit your changes: `git commit -am 'Add amazing feature'`
5. Push to the branch: `git push origin feature/amazing-feature`
6. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Authors

- Roman Geller - roma.geller@mail.ru

## Acknowledgments

- Central Bank of Russia for providing the currency API
- FastAPI team for the excellent web framework and documentation
- Python community for the rich ecosystem of development tools
- Poetry team for modern Python dependency management