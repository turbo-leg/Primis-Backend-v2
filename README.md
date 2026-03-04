# Primis Educare API

Primis Educare is an educational platform backend API built with modern Python technologies. 

## Tech Stack
- **Framework:** FastAPI
- **Database:** PostgreSQL
- **ORM:** SQLAlchemy 2.0
- **Migrations:** Alembic
- **Authentication:** JWT, bcrypt

## Local Setup

### Using Docker (Recommended)
You can quickly run the application and its database using Docker.

1. Create a `.env` file in the root directory and add the following database credentials:
   ```env
   POSTGRES_SERVER=db
   POSTGRES_USER=postgres
   POSTGRES_PASSWORD=postgres
   POSTGRES_DB=primis
   DATABASE_URL=postgresql+asyncpg://postgres:postgres@db:5432/primis
   ```
2. Build and run the containers:
   ```bash
   docker-compose up --build
   ```

### Local Development (Without Docker)

1. **Clone and Virtual Environment**
   ```bash
   python -m venv venv
   source venv/bin/activate
   ```

2. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Database Setup**
   Ensure PostgreSQL is running locally. Set the `DATABASE_URL` environment variable or add it to your `.env` file:
   ```env
   DATABASE_URL=postgresql+asyncpg://<user>:<password>@localhost:5432/<dbname>
   ```

4. **Run Migrations**
   Initialize your database schema:
   ```bash
   alembic upgrade head
   ```

5. **Start the Server**
   ```bash
   uvicorn app.main:app --reload
   ```

The API documentation will be available at `http://localhost:8000/docs`.

## Testing
Run the test suite using `pytest`:
```bash
pytest
```
