# Create virtual environment
python3 -m venv .venv
source .venv/bin/activate  # Linux/Mac
# .venv\Scripts\activate   # Windows

# Install dependencies
pip install fastapi uvicorn scalar-fastapi
```

## 2. Run the Server

```bash
uvicorn main:app --reload
```

Server will start at `http://localhost:8000`

## 3. API Documentation

- **Interactive Docs**: [http://localhost:8000/docs](http://localhost:8000/docs)
- **Scalar Docs**: [http://localhost:8000/scalar](http://localhost:8000/scalar)

## 4. Endpoints

| Method | Path | Description |
|--------|------|-------------|
| `GET` | `/shipments/{shipment_id}` | Get shipment by ID |
| `POST` | `/shipments` | Create new shipment |
| `PATCH` | `/shipments` | Update shipment |
| `DELETE` | `/shipments` | Delete shipment |
| `GET` | `/scalar` | Scalar API reference |

## 5. Example Requests

### Create Shipment

```bash
curl -X POST "http://localhost:8000/shipments" \
     -H "Content-Type: application/json" \
     -d '{"weight": 2.5, "content": "books", "status": "placed"}'
```

### Get Shipment

```bash
curl "http://localhost:8000/shipments/12701"
```

### Update Shipment

```bash
curl -X PATCH "http://localhost:8000/shipments?id=12701" \
     -H "Content-Type: application/json" \
     -d '{"status": "shipped"}'
```

### Delete Shipment

```bash
curl -X DELETE "http://localhost:8000/shipments?id=12701"