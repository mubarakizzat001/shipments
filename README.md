# 📦 Shipment Management API

A FastAPI-based REST API for managing shipments using SQLModel for database interactions and Pydantic for data validation.

## 🚀 Features

- ✅ CRUD operations for shipments
- ✅ Database persistence with SQLite and SQLModel
- ✅ Data validation with Pydantic
- ✅ Interactive API documentation (Swagger & Scalar)
- ✅ Type hints and response models
- ✅ Status tracking for shipments
- ✅ Weight and content validation

## 📋 Requirements

- Python 3.8+
- FastAPI
- SQLModel
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

## 🏃 Running the Application

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

```python
- placed
- shipped
- in_transit
- delivered
- returned
```

### CreateShipment

```json
{
  "weight": 2.5,
  "content": "books",
  "destination": "Cairo, Egypt"
}
```

**Validation Rules:**
- `weight`: Must be ≤ 15 kg
- `content`: 5-50 characters

### UpdateShipment

All fields are optional:

```json
{
  "status": "shipped",
  "estimated_delivery": "2026-02-10T12:00:00"
}
```

### ReadShipment

Response model includes all fields plus status and estimated delivery:

```json
{
  "id": 1,
  "weight": 2.5,
  "content": "books",
  "destination": "Cairo, Egypt",
  "status": "placed",
  "estimated_delivery": "2026-02-06T20:22:34"
}
```

## 💡 Usage Examples

### Create a Shipment

```bash
curl -X POST "http://127.0.0.1:8000/shipments" \
     -H "Content-Type: application/json" \
     -d '{
       "weight": 2.5,
       "content": "magic books",
       "destination": "Alexandria"
     }'
```

### Get a Shipment

```bash
curl "http://127.0.0.1:8000/shipments/1"
```

### Update a Shipment

```bash
curl -X PATCH "http://127.0.0.1:8000/shipments/1" \
     -H "Content-Type: application/json" \
     -d '{
       "status": "shipped"
     }'
```

### Delete a Shipment

```bash
curl -X DELETE "http://127.0.0.1:8000/shipments/1"
```

## 📁 Project Structure

```
ml_fastapi/
├── main.py           # FastAPI application and endpoints
├── schemas.py        # Pydantic models for request/response
├── database/
│   ├── models.py     # SQLModel database tables
│   └── session.py    # Database engine and session configuration
├── requirements.txt  # Project dependencies
├── sqlite.db         # SQLite database file
└── README.md         # This file
```

## ⚙️ Configuration

The application uses **SQLModel** with **SQLite** for data persistence. The database is stored locally in `sqlite.db`.

## 🐛 Error Handling

The API returns appropriate HTTP status codes:

- `200 OK`: Successful request
- `404 Not Found`: Shipment not found
- `400 Bad Request`: Missing update data
- `422 Unprocessable Entity`: Validation error

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

- FastAPI framework
- SQLModel for easy ORM
- Scalar for beautiful API documentation
