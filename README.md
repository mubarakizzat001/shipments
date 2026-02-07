# 📦 Shipment Management API

A modern, modular FastAPI REST API for creating and tracking shipments. This project features a clean architecture, asynchronous database operations, and secure authentication.

---

## 🚀 Key Features

- **Modular architecture**: Organized into API (routers, schemas), Services, and Database layers.
- **Async DB operations**: Utilizes SQLModel with `asyncpg` for efficient PostgreSQL interactions.
- **JWT-based Authentication**: Secure seller account management with token-based access control.
- **Auto Table Creation**: Automatically sets up database tables on startup.
- **Interactive Documentation**: Swagger UI and **Scalar** API reference for better developer experience.

---

## 📋 Requirements

- Python 3.9+
- See `requirements.txt` for dependencies:
  - `fastapi`, `uvicorn`, `sqlmodel`, `asyncpg`
  - `passlib[bcrypt]`, `pyjwt`
  - `scalar-fastapi`, `pydantic-settings`

---

## ⚙️ Environment variables (.env)

Create a `.env` file at the project root based on `.env.example`:

```ini
POSTGRES_SERVER=localhost
POSTGRES_PORT=5432
POSTGRES_USER=your_user
POSTGRES_PASSWORD=your_password
POSTGRES_DB=shipment_db
JWT_SECRET=your_jwt_secret
JWT_ALGORITHM=HS256
```

---

## 🛠 Installation

1. Clone and enter project directory:
   ```bash
   git clone <repo-url>
   cd ml_fastapi
   ```

2. Create and activate a virtual environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

---

## ▶️ Running the API

Start the server from the project root:

```bash
uvicorn ml_fastapi.main:app --reload
```

- **Swagger UI**: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
- **Scalar Docs**: [http://127.0.0.1:8000/scalar](http://127.0.0.1:8000/scalar)

---

## 🔌 API Endpoints

### Seller (Authentication)
| Method | Endpoint | Description | Auth |
| :--- | :--- | :--- | :--- |
| `POST` | `/seller/signup` | Register a new seller | No |
| `POST` | `/seller/login` | Login (OAuth2 Password Grant) | No |
| `GET` | `/seller/dashboard` | Access protected seller dashboard | Bearer Token |

### Shipments
| Method | Endpoint | Description | Auth |
| :--- | :--- | :--- | :--- |
| `POST` | `/api/` | Create a new shipment | No |
| `GET` | `/api/` | Get shipment by ID (requires `shipment_id` query param) | No |
| `PATCH` | `/api/` | Update shipment (partial, requires `shipment_id`) | No |
| `DELETE` | `/api/` | Delete shipment (requires `shipment_id`) | No |

---

## 🔐 Authentication Example (curl)

1. **Signup**:
   ```bash
   curl -X POST "http://127.0.0.1:8000/seller/signup" -H "Content-Type: application/json" -d '{"name": "Alice", "email": "a@example.com", "password": "secret"}'
   ```

2. **Login**:
   ```bash
   curl -X POST "http://127.0.0.1:8000/seller/login" -H "Content-Type: application/x-www-form-urlencoded" -d "username=a@example.com&password=secret"
   ```

3. **Dashboard Access**:
   ```bash
   curl -H "Authorization: Bearer <your_jwt_token>" http://127.0.0.1:8000/seller/dashboard
   ```

---

## 🗂 Project Structure

```text
ml_fastapi/
├── api/             # API Layer (routers, schemas)
├── core/            # Core settings and security
├── database/        # DB session and SQLModel models
├── services/        # Business logic (Seller, Shipment)
├── main.py          # FastAPI application entry point
└── utils.py         # Helper functions (JWT, security)
```

---

## 🧪 Testing

Run tests using:
```bash
pytest
```

---

## 🤝 Contributing

Contributions are welcome! Please fork the repository and submit a pull request.

---

## 📄 License

MIT
