# 📦 Shipment Management API

A modern, modular FastAPI-based REST API for managing shipments using SQLModel for database interactions, async PostgreSQL for persistence, and Pydantic for data validation.

## 🚀 Features

- ✅ **Modular Architecture**: Clean separation of concerns (API, Services, Database).
- ✅ **Async Operations**: Fully asynchronous database interactions using `SQLAlchemy` and `asyncpg`.
- ✅ **Database Persistence**: Robust persistence with PostgreSQL and SQLModel.
- ✅ **Interactive Documentation**: Beautiful API reference with Scalar and standard Swagger UI.
- ✅ **Environment-based Config**: Flexible configuration using `pydantic-settings`.
- ✅ **Data Validation**: Strict type-safe data handling with Pydantic.
- ✅ **Shipment Tracking**: Comprehensive CRUD for shipments with status and delivery estimation.

## 📋 Requirements

- Python 3.9+
- FastAPI
- SQLModel
- PostgreSQL (with `asyncpg`)
- Pydantic Settings
- Scalar FastAPI

## 🛠️ Installation

### 1. Clone the repository

```bash
git clone https://github.com/mubarakizzat001/shipments.git
cd ml_fastapi
```

### 2. Create virtual environment

```bash
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate   # Windows
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configuration

Copy the example environment file and update it with your PostgreSQL credentials:

```bash
cp .env.example .env
```

Edit `.env`:
```ini
POSTGRES_SERVER=localhost
POSTGRES_PORT=5432
POSTGRES_USER=your_user
POSTGRES_PASSWORD=your_password
POSTGRES_DB=shipment_db
```

## 跑步 Running the Application

### Development Mode

```bash
fastapi dev
```

The server will start at `http://127.0.0.1:8000`

### Production Mode

```bash
fastapi run
```

## 📚 API Documentation

Once the server is running, access the documentation at:

- **Swagger UI**: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
- **Scalar UI**: [http://127.0.0.1:8000/scalar](http://127.0.0.1:8000/scalar)

## 🔌 API Endpoints

| Method | Endpoint | Description | Request Body |
|--------|----------|-------------|--------------|
| `GET` | `/shipments/{shipment_id}` | Get shipment by ID | - |
| `POST` | `/shipments` | Create new shipment | `CreateShipment` |
| `PATCH` | `/shipments/{shipment_id}` | Update shipment | `UpdateShipment` |
| `DELETE` | `/shipments/{shipment_id}` | Delete shipment | - |
| `GET` | `/scalar` | Scalar API reference | - |

## 📦 Data Models

### ShipmentStatus (Enum)

- `placed`: Shipment order received.
- `shipped`: Shipment has left the origin.
- `in_transit`: Shipment is on its way.
- `delivered`: Shipment has arrived.
- `returned`: Shipment was returned to sender.

### CreateShipment
Required fields inherited from `BaseShipment`:
- `weight`: float (max 15 kg)
- `content`: string (5-50 chars)
- `destination`: string (optional)

### UpdateShipment
All fields are optional:
- `weight`: New weight
- `content`: New description
- `destination`: New destination
- `status`: New `ShipmentStatus`
- `estimated_delivery`: New datetime

## 📁 Project Structure

```
ml_fastapi/
├── api/
│   ├── dependencies.py    # Service and Session dependencies
│   ├── router.py          # API route definitions
│   └── schemas/           # Pydantic/SQLModel schemas
│       └── shipment.py    # Shipment models
├── database/
│   ├── models.py          # Enums and base models
│   └── session.py         # Async engine and session setup
├── services/
│   └── shipment.py        # Business logic and DB operations
├── config.py              # Environment and app configuration
├── main.py                # Application entry point & lifespan
├── requirements.txt       # Python dependencies
└── .env                   # Configuration variables
```

## ⚙️ Configuration

The application uses **SQLModel** with **Async PostgreSQL**. Database tables are automatically created on startup via the `lifespan` handler in `main.py`.

## 🐛 Error Handling

The API returns appropriate HTTP status codes:

- `200 OK`: Successful request.
- `201 Created`: Successfully created a resource.
- `400 Bad Request`: Validation error or missing data.
- `404 Not Found`: Shipment not found.
- `422 Unprocessable Entity`: Invalid request parameters.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License.

## 👨‍💻 Author

Mubarak Izzat

## 🙏 Acknowledgments

- [FastAPI](https://fastapi.tiangolo.com/)
- [SQLModel](https://sqlmodel.tiangolo.com/)
- [Scalar](https://scalar.com/) for beautiful API documentation.
