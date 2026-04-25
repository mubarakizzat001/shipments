# 📦 Shipment Management API

A modern, modular FastAPI REST API for creating and tracking shipments. This project features a clean architecture, asynchronous database operations, and secure authentication.

---

## 🚀 Key Features

- **Modular architecture**: Organized into API (routers, schemas), Services, and Database layers.
- **Async DB operations**: Utilizes SQLModel with `asyncpg` for efficient PostgreSQL interactions.
- **Database Migrations**: Managed via **Alembic** for seamless schema evolution.
- **JWT-based Authentication**: Secure seller account management with token-based access control.
- **Token Blacklisting via Redis**: Logout invalidates JWT tokens instantly using a Redis-backed blacklist (JTI-based).
- **Secure Logout**: `/seller/logout` endpoint blacklists the token's JTI, preventing reuse even before expiry.
- **Auto Table Creation**: Automatically sets up database tables on startup.
- **Interactive Documentation**: Swagger UI and **Scalar** API reference for better developer experience.

---

## 📋 Requirements

- Python 3.9+
- Redis server (for token blacklisting)
- See `requirements.txt` for dependencies:
  - `fastapi[all]`, `uvicorn`, `sqlmodel`, `asyncpg`, `alembic`
  - `passlib[bcrypt]`, `pyjwt`
  - `scalar-fastapi`, `pydantic-settings`
  - `redis` (async Redis client)

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

# Redis (for token blacklisting)
REDIS_HOST=localhost
REDIS_PORT=6379
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

4. Run migrations:
   ```bash
   alembic upgrade head
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
| `POST` | `/seller/logout` | Logout and blacklist current JWT token | Bearer Token |

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

4. **Logout** (blacklists the token via Redis):
   ```bash
   curl -X POST -H "Authorization: Bearer <your_jwt_token>" http://127.0.0.1:8000/seller/logout
   ```

---

## 🗂 Project Structure

```text
ml_fastapi/
├── app/
│   ├── api/
│   │   ├── routers/         # Route handlers (seller, shipment)
│   │   ├── schemas/         # Pydantic request/response schemas
│   │   └── dependencies.py  # Shared FastAPI dependencies
│   ├── core/
│   │   └── security.py      # OAuth2 scheme
│   ├── database/
│   │   ├── models.py        # SQLModel ORM models (Shipment, Seller)
│   │   ├── session.py       # Async DB session & table creation
│   │   └── redis.py         # Redis client for token blacklisting
│   ├── services/            # Business logic (Seller, Shipment)
│   ├── config.py            # Pydantic settings (DB + Redis + JWT)
│   ├── main.py              # FastAPI application entry point
│   ├── requirements.txt     # Project dependencies
│   └── utils.py             # JWT encode/decode helpers
├── migrations/
│   ├── versions/            # Alembic migration scripts
│   │   ├── e631a51dfd79_init.py
│   │   └── a5da181bdee1_add_updated_at.py
│   ├── env.py               # Alembic async migration environment
│   └── script.py.mako       # Migration script template
└── alembic.ini              # Alembic configuration file
```

---

## 🗃 Database Migrations (Alembic)

This project uses **Alembic** with full async support for managing database schema changes.

### Create a new migration
```bash
alembic revision --autogenerate -m "describe your change"
```

### Apply migrations
```bash
alembic upgrade head
```

### Rollback last migration
```bash
alembic downgrade -1
```

> **Note:** `migrations/env.py` is configured to use the async PostgreSQL engine from `app.config`, so migrations run against the same database as the app.

---

## 📐 Data Models

### Shipment
| Field | Type | Description |
| :--- | :--- | :--- |
| `id` | UUID | Auto-generated primary key |
| `content` | str | Description of shipment contents |
| `weight` | float | Weight in kg (max 25 kg) |
| `destination` | int | Destination identifier |
| `status` | ShipmentStatus | `placed`, `shipped`, `in_transit`, `delivered`, `returned` |
| `estimated_delivery` | datetime | Estimated delivery date (auto-set to +5 days) |
| `created_at` | datetime | Timestamp when shipment was created |
| `updated_at` | datetime | ⭐ **New** — Timestamp of the last update |
| `seller_id` | UUID | Foreign key linking to the Seller |

### Seller
| Field | Type | Description |
| :--- | :--- | :--- |
| `id` | UUID | Auto-generated primary key |
| `name` | str | Seller display name |
| `email` | EmailStr | Seller email address |
| `password` | str | Hashed password (excluded from responses) |
| `created_at` | datetime | Timestamp when seller account was created |

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
