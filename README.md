# 📦 Shipment Management API

A modern, modular FastAPI REST API for creating and tracking shipments. This project features a clean layered architecture, asynchronous database operations, a full shipment lifecycle with event tracking, automatic delivery partner assignment, and secure dual authentication for Sellers and Delivery Partners.

---

## 🚀 Key Features

- **Modular architecture**: Organized into API (routers, schemas), Services, and Database layers.
- **Async DB operations**: Utilizes SQLModel with `asyncpg` for efficient PostgreSQL interactions.
- **Database Migrations**: Managed via **Alembic** for seamless schema evolution.
- **JWT-based Authentication**: Secure account management for both **Sellers** and **Delivery Partners** with token-based access control.
- **Dual OAuth2 schemes**: Separate OAuth2 password flows for Sellers (`/seller/login`) and Delivery Partners (`/deliverypartner/login`).
- **Token Blacklisting via Redis**: Logout immediately invalidates JWT tokens using a Redis-backed JTI blacklist.
- **Secure Logout**: Both `/seller/logout` and `/deliverypartner/logout` blacklist the token's JTI, preventing reuse even before expiry.
- **Auto Delivery Partner Assignment**: On shipment creation, the system automatically assigns an eligible delivery partner based on destination zip code and available capacity.
- **Shipment Event Timeline**: Every status change is recorded as a `ShipmentEvent`, forming a full audit timeline per shipment.
- **Shipment Cancellation**: Sellers can cancel their own shipments; the cancellation is recorded in the event timeline.
- **Auto Table Creation**: Automatically sets up database tables on startup.
- **Interactive Documentation**: Swagger UI and **Scalar** API reference for a better developer experience.

---

## 📋 Requirements

- Python 3.9+
- Redis server (for token blacklisting)
- PostgreSQL database
- See `requirements.txt` for dependencies:
  - `fastapi[all]`, `uvicorn`, `sqlmodel`, `asyncpg`, `alembic`
  - `passlib[bcrypt]`, `pyjwt`, `bcrypt`
  - `scalar-fastapi`, `pydantic-settings`
  - `redis` (async Redis client)

---

## ⚙️ Environment Variables (.env)

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
   pip install -r app/requirements.txt
   ```

4. Run migrations:
   ```bash
   alembic upgrade head
   ```

---

## ▶️ Running the API

Start the server from the project root:

```bash
uvicorn app.main:app --reload
```

- **Swagger UI**: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
- **Scalar Docs**: [http://127.0.0.1:8000/scalar](http://127.0.0.1:8000/scalar)

---

## 🔌 API Endpoints

### Seller (Authentication)
| Method | Endpoint | Description | Auth |
| :--- | :--- | :--- | :--- |
| `POST` | `/seller/signup` | Register a new seller (with `address` & `zip_code`) | No |
| `POST` | `/seller/login` | Login (OAuth2 Password Grant) | No |
| `POST` | `/seller/logout` | Logout and blacklist current JWT token | Bearer Token (Seller) |

### Shipments
| Method | Endpoint | Description | Auth |
| :--- | :--- | :--- | :--- |
| `POST` | `/api/` | Create a new shipment (auto-assigns delivery partner) | Bearer Token (Seller) |
| `GET` | `/api/` | Get shipment by ID (`shipment_id` query param) | Bearer Token (Seller) |
| `PATCH` | `/api/` | Update shipment status/location (delivery partner only) | Bearer Token (Delivery Partner) |
| `GET` | `/api/cancel` | Cancel a shipment by ID (seller only, records event) | Bearer Token (Seller) |

### Delivery Partner
| Method | Endpoint | Description | Auth |
| :--- | :--- | :--- | :--- |
| `POST` | `/deliverypartner/signup` | Register a new delivery partner | No |
| `POST` | `/deliverypartner/login` | Login (OAuth2 Password Grant) | No |
| `POST` | `/deliverypartner/update` | Update capacity or serviceable zip codes | Bearer Token (Delivery Partner) |
| `GET` | `/deliverypartner/logout` | Logout and blacklist current JWT token | Bearer Token (Delivery Partner) |

---

## 🔐 Authentication Examples (curl)

### Seller

1. **Signup**:
   ```bash
   curl -X POST "http://127.0.0.1:8000/seller/signup" \
     -H "Content-Type: application/json" \
     -d '{"name": "Alice", "email": "alice@example.com", "password": "secret", "address": "123 Main St", "zip_code": 10001}'
   ```

2. **Login**:
   ```bash
   curl -X POST "http://127.0.0.1:8000/seller/login" \
     -H "Content-Type: application/x-www-form-urlencoded" \
     -d "username=alice@example.com&password=secret"
   ```

3. **Logout** (blacklists the token via Redis):
   ```bash
   curl -X POST -H "Authorization: Bearer <your_jwt_token>" http://127.0.0.1:8000/seller/logout
   ```

### Delivery Partner

1. **Signup**:
   ```bash
   curl -X POST "http://127.0.0.1:8000/deliverypartner/signup" \
     -H "Content-Type: application/json" \
     -d '{"name": "FastShip", "email": "partner@example.com", "password": "secret", "max_handling_capacity": 10, "servicable_zip_codes": [10001, 10002]}'
   ```

2. **Login**:
   ```bash
   curl -X POST "http://127.0.0.1:8000/deliverypartner/login" \
     -H "Content-Type: application/x-www-form-urlencoded" \
     -d "username=partner@example.com&password=secret"
   ```

3. **Update capacity/zip codes**:
   ```bash
   curl -X POST "http://127.0.0.1:8000/deliverypartner/update" \
     -H "Authorization: Bearer <partner_jwt_token>" \
     -H "Content-Type: application/json" \
     -d '{"max_handling_capacity": 15}'
   ```

### Shipments

1. **Create a shipment** (auto-assigns delivery partner):
   ```bash
   curl -X POST "http://127.0.0.1:8000/api/" \
     -H "Authorization: Bearer <seller_jwt_token>" \
     -H "Content-Type: application/json" \
     -d '{"content": "Books and stationery", "weight": 2.5, "destination": 10001}'
   ```

2. **Cancel a shipment**:
   ```bash
   curl -X GET "http://127.0.0.1:8000/api/cancel?id=<shipment_uuid>" \
     -H "Authorization: Bearer <seller_jwt_token>"
   ```

---

## 🗂 Project Structure

```text
ml_fastapi/
├── app/
│   ├── api/
│   │   ├── routers/
│   │   │   ├── seller.py           # Seller auth endpoints
│   │   │   ├── shipment.py         # Shipment CRUD + cancel endpoints
│   │   │   └── delivery_partner.py # Delivery partner auth & update endpoints
│   │   ├── schemas/
│   │   │   ├── seller.py           # Seller request/response schemas
│   │   │   ├── shipment.py         # Shipment request/response schemas
│   │   │   └── delivery_partner.py # DeliveryPartner request/response schemas
│   │   ├── dependencies.py         # Shared FastAPI dependencies & DI wiring
│   │   └── router.py               # Master router (combines all routers)
│   ├── core/
│   │   └── security.py             # Dual OAuth2 schemes (Seller + DeliveryPartner)
│   ├── database/
│   │   ├── models.py               # SQLModel ORM models (Shipment, Seller, DeliveryPartner, ShipmentEvent)
│   │   ├── session.py              # Async DB session & table creation
│   │   └── redis.py                # Redis client for token blacklisting
│   ├── services/
│   │   ├── Base_Service.py         # Generic async CRUD base (get, add, patch, delete)
│   │   ├── Base_User.py            # Base user logic (register, hash password, login, JWT)
│   │   ├── seller.py               # Seller-specific service
│   │   ├── shipment.py             # Shipment business logic (create, update, cancel, delete)
│   │   ├── ShipmentEventService.py # Shipment event tracking & auto-description generation
│   │   └── DeliveryPartnerService.py # Partner registration, login, zip-code assignment
│   ├── config.py                   # Pydantic settings (DB + Redis + JWT)
│   ├── main.py                     # FastAPI application entry point
│   ├── requirements.txt            # Project dependencies
│   └── utils.py                    # JWT encode/decode helpers
├── migrations/
│   ├── versions/                   # Alembic migration scripts
│   ├── env.py                      # Alembic async migration environment
│   └── script.py.mako              # Migration script template
└── alembic.ini                     # Alembic configuration file
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
| `content` | str | Description of shipment contents (5–50 chars) |
| `weight` | float | Weight in kg (max 25 kg) |
| `destination` | int | Destination zip code |
| `status` | ShipmentStatus | Derived from latest event: `placed`, `shipped`, `in_transit`, `delivered`, `returned`, `cancelled` |
| `estimated_delivery` | datetime | Estimated delivery date (auto-set to +5 days on creation) |
| `created_at` | datetime | Timestamp when shipment was created |
| `updated_at` | datetime | Timestamp of the last update |
| `seller_id` | UUID | Foreign key linking to the Seller |
| `delivery_partner_id` | UUID | Foreign key linking to the assigned DeliveryPartner |
| `timeline` | list[ShipmentEvent] | Ordered list of all status change events |

### ShipmentEvent ⭐ New
| Field | Type | Description |
| :--- | :--- | :--- |
| `id` | UUID | Auto-generated primary key |
| `shipment_id` | UUID | Foreign key linking to the Shipment |
| `status` | ShipmentStatus | Status recorded at this event |
| `location` | int | Zip code location where the event occurred |
| `description` | str | Auto-generated or custom event description |
| `created_at` | datetime | Timestamp when this event was recorded |

### Seller
| Field | Type | Description |
| :--- | :--- | :--- |
| `id` | UUID | Auto-generated primary key |
| `name` | str | Seller display name |
| `email` | EmailStr | Seller email address |
| `password` | str | Hashed password (excluded from responses) |
| `address` | str | ⭐ **New** — Seller's physical address |
| `zip_code` | int | ⭐ **New** — Seller's zip code (used as origin location for events) |
| `created_at` | datetime | Timestamp when seller account was created |
| `updated_at` | datetime | Timestamp of the last update |

### DeliveryPartner ⭐ New
| Field | Type | Description |
| :--- | :--- | :--- |
| `id` | UUID | Auto-generated primary key |
| `name` | str | Partner display name |
| `email` | EmailStr | Partner email address |
| `password` | str | Hashed password (excluded from responses) |
| `max_handling_capacity` | int | Maximum number of shipments the partner can handle |
| `servicable_zip_codes` | list[int] | List of zip codes the partner can deliver to |
| `created_at` | datetime | Timestamp when partner account was created |
| `updated_at` | datetime | Timestamp of the last update |

> **Computed properties on `DeliveryPartner`:**
> - `active_shipments` — shipments not yet delivered or cancelled
> - `current_handling_capacity` — `max_handling_capacity - len(active_shipments)`

---

## 🔄 Shipment Lifecycle

```
[Seller creates shipment]
        │
        ▼
   status: placed  ──────────────────────────────────────► [cancelled] ← Seller can cancel
        │
        ▼ (Delivery Partner updates)
   status: shipped
        │
        ▼
   status: in_transit
        │
        ▼
   status: delivered / returned
```

Each transition is recorded as a `ShipmentEvent` in the `timeline` with a location, status, and auto-generated description.

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
