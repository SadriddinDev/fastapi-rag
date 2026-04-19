# FastAPI RAG

A production-ready **Retrieval-Augmented Generation (RAG)** API built with FastAPI, PostgreSQL, ChromaDB, and a local Ollama LLM — fully containerized with Docker.

## Features

- JWT authentication (access + refresh tokens)
- Product CRUD with image support
- PDF ingestion and semantic search via ChromaDB
- Local LLM inference using Ollama (`llama3.2:1b`)
- Sentence embeddings with `all-MiniLM-L6-v2`
- Async PostgreSQL with SQLAlchemy + Alembic migrations

## Tech Stack

| Layer | Technology |
|---|---|
| API | FastAPI |
| Database | PostgreSQL 16 |
| Vector store | ChromaDB |
| Embeddings | sentence-transformers (`all-MiniLM-L6-v2`) |
| LLM | Ollama (`llama3.2:1b`) |
| Auth | JWT (python-jose) |
| Migrations | Alembic |
| Container | Docker + Docker Compose |

## Project Structure

```
app/
├── api/v1/
│   ├── routes.py          # Auth endpoints (register, login, refresh, logout, me)
│   ├── product_routes.py  # Product CRUD
│   └── rag_routes.py      # RAG endpoints (upload PDF, ask question)
├── core/
│   ├── config.py          # Settings from .env
│   ├── deps.py            # JWT dependency injection
│   └── security.py        # Password hashing, token creation
├── db/                    # SQLAlchemy session + base
├── models/                # User, Product, ProductImage ORM models
├── rag/
│   ├── embeddings.py      # Sentence-transformer embedding
│   ├── ingestion.py       # PDF parsing and indexing into ChromaDB
│   ├── retrieval.py       # Semantic search from ChromaDB
│   ├── llm.py             # Ollama inference call
│   └── vectorstore.py     # ChromaDB client setup
├── repositories/          # DB query layer
├── schemas/               # Pydantic request/response models
├── services/              # Business logic layer
└── main.py                # FastAPI app entry point
```

## Getting Started

### Prerequisites

- Docker and Docker Compose

### 1. Clone the repo

```bash
git clone <repo-url>
cd fastapi-rag
```

### 2. Configure environment

Create a `.env` file:

```env
SECRET_KEY=your-secret-key
DATABASE_URL=postgresql+asyncpg://fastapi:fastapi@db:5432/fastapi_db
```

### 3. Start services

```bash
docker compose up --build
```

This starts three services:
- `api` — FastAPI app on port `8000`
- `db` — PostgreSQL on port `5432`
- `ollama` — Local LLM server on port `11434` (auto-pulls `llama3.2:1b`)

### 4. Run migrations

```bash
docker compose exec api alembic upgrade head
```

## API Endpoints

### Auth — `/api/v1`

| Method | Path | Description |
|---|---|---|
| POST | `/users` | Register a new user |
| POST | `/login` | Login, returns access + refresh tokens |
| POST | `/refresh` | Refresh access token |
| POST | `/logout` | Logout (client deletes tokens) |
| GET | `/me` | Get current user info |

### Products — `/api/v1/products`

| Method | Path | Description |
|---|---|---|
| GET | `/` | List all products |
| POST | `/` | Create a product |
| GET | `/{id}` | Get a product |
| PUT | `/{id}` | Update a product |
| DELETE | `/{id}` | Delete a product |

### RAG — `/api/v1/rag`

> All RAG endpoints require a valid Bearer token.

| Method | Path | Description |
|---|---|---|
| POST | `/upload` | Upload a PDF to index into ChromaDB |
| POST | `/ask` | Ask a question answered from indexed documents |

### Example: Ask a question

```bash
curl -X POST "http://localhost:8000/api/v1/rag/ask?question=What is the refund policy?" \
  -H "Authorization: Bearer <your-token>"
```

## How RAG Works

1. **Ingest** — Upload a PDF; text is extracted, split into chunks, embedded with `all-MiniLM-L6-v2`, and stored in ChromaDB.
2. **Retrieve** — On a question, the query is embedded and the top-k most similar chunks are fetched from ChromaDB.
3. **Generate** — The retrieved chunks are passed as context to Ollama (`llama3.2:1b`), which generates a grounded answer.

## Interactive Docs

Once running, visit [http://localhost:8000/docs](http://localhost:8000/docs) for the Swagger UI.
