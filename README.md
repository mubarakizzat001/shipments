# 📦 Shipment Management API

A FastAPI-based REST API for managing shipments with validation using Pydantic models.

## 🚀 Features

- ✅ CRUD operations for shipments
- ✅ Data validation with Pydantic
- ✅ Interactive API documentation (Swagger & Scalar)
- ✅ Type hints and response models
- ✅ Status tracking for shipments
- ✅ Weight and content validation

## 📋 Requirements

- Python 3.8+
- FastAPI
- Uvicorn
- Pydantic
- Scalar FastAPI

## 🛠️ Installation

### 1. Clone the repository

```bash
git clone <your-repo-url>
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
- **OpenAPI JSON**: [http://127.0.0.1:8000/openapi.json](http://127.0.0.1:8000/openapi.json)

## 🔌 API Endpoints

| Method | Endpoint | Description | Request Body |
|--------|----------|-------------|--------------|
| `GET` | `/shipments/{shipment_id}` | Get shipment by ID | - |
| `POST` | `/shipments` | Create new shipment | `create_shipment` |
| `PATCH` | `/shipments?id={id}` | Update shipment | `update_shipment` |
| `DELETE` | `/shipments?id={id}` | Delete shipment | - |
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

### create_shipment

```json
{
  "weight": 2.5,
  "content": "books",
  "destination": 12345
}
```

**Validation Rules:**
- `weight`: Must be ≤ 15 kg
- `content`: 5-50 characters
- `destination`: Integer (destination ID)

### update_shipment

All fields are optional:

```json
{
  "weight": 3.0,
  "content": "updated content",
  "destination": 54321,
  "status": "shipped"
}
```

### read_shipment

Response model includes all fields plus status:

```json
{
  "weight": 2.5,
  "content": "books",
  "destination": 12345,
  "status": "placed"
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
       "destination": 12345
     }'
```

**Response:**
```json
{
  "id": 12706
}
```

### Get a Shipment

```bash
curl "http://127.0.0.1:8000/shipments/12701"
```

**Response:**
```json
{
  "weight": 0.6,
  "content": "rubber ducks",
  "destination": 0,
  "status": "placed"
}
```

### Update a Shipment

```bash
curl -X PATCH "http://127.0.0.1:8000/shipments?id=12701" \
     -H "Content-Type: application/json" \
     -d '{
       "status": "shipped"
     }'
```

**Response:**
```json
{
  "weight": 0.6,
  "content": "rubber ducks",
  "status": "shipped",
  "destination": 0
}
```

### Delete a Shipment

```bash
curl -X DELETE "http://127.0.0.1:8000/shipments?id=12701"
```

**Response:**
```json
{
  "message": "shipment 12701 deleted"
}
```

## 📁 Project Structure

```
ml_fastapi/
├── main.py           # FastAPI application and endpoints
├── schemas.py        # Pydantic models and validation
├── requirements.txt  # Project dependencies
├── __init__.py      # Package initialization
└── README.md        # This file
```

## ⚙️ Configuration

The application uses an in-memory dictionary for data storage. For production use, consider integrating a database like PostgreSQL or MongoDB.

## 🔒 Validation Rules

- **Weight**: Maximum 15 kg
- **Content**: Between 5 and 50 characters
- **Status**: Must be one of the predefined enum values
- **Destination**: Integer value

## 🐛 Error Handling

The API returns appropriate HTTP status codes:

- `200 OK`: Successful request
- `404 Not Found`: Shipment not found
- `406 Not Acceptable`: Shipment too heavy (>15kg)
- `422 Unprocessable Entity`: Validation error

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 👨‍💻 Author

Mubarak Izzat

## 🙏 Acknowledgments

- FastAPI framework
- Pydantic for data validation
- Scalar for beautiful API documentation
