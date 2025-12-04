# Billacy

Billacy is a lightweight Python application for managing users, invoices, and student classes. It provides a simple GUI interface built with Tkinter, uses SQLAlchemy for database interaction, and Alembic for migrations.

---

## Features

- Manage **users**, **invoices**, and **student classes**.
- Add, remove, and view records via a Tkinter GUI.
- Service-based architecture separates business logic from the UI.
- Database schema migrations via **Alembic**.
- Supports MySQL database.

---

## Tech Stack

- **Python 3.11+**
- **Tkinter** for GUI
- **SQLAlchemy** ORM
- **Alembic** for database migrations
- **MySQL** / **MySQL Connector**
- **PyInstaller** (optional) for building an executable

---

## Installation

### Clone the repository

```bash
git clone <repo-url>
cd billacy
```

### Create a virtual environment and install dependencies

```bash
python -m venv .venv
source .venv/bin/activate   # Linux/macOS
.venv\Scripts\activate      # Windows
pip install -r requirements.txt
```
## Environment Variables
Create `.env.development.local` or `.env.test.local` and add:

```dotenv
ENV=development
MYSQL_DB_USER=<your_user>
MYSQL_DB_PASSWORD=<your_password>
MYSQL_DB_HOST=localhost
MYSQL_DB_PORT=3306
MYSQL_DB_NAME=billacy
```

## Database Setup
1. Initialize the database schema:
```bash
alembic upgrade head
```

2. Create new migrations automatically after model changes:
```bash
alembic revision --autogenerate -m "Migration description"
alembic upgrade head
```

## Running the App

```bash
python main.py
```
This launches the Tkinter GUI.

## Project Structure

```bash
.app/
├───assets/
│   └───images/          # project assets like images
├───connection/          # database connection setup
├───gui/
│   ├───pages/           # GUI pages
├───models/              # SQLAlchemy models
├───repositories/        # database access logic
├───services/            # business logic
├───tests/               # unit tests
├───utils/               # utility functions

.migrations/
├───versions/            # Alembic migration scripts

.docker_compose/         # docker-compose files if any

main.py                  # entry point of the app
requirements.txt
README.md
.gitignore
```

## Creating an Executable (Optional)

To provide the app as an `.exe` for end users:
```bash
pyinstaller --onefile main.py
```

The executable will be in the `dist/` folder.

## Notes

- Keep migration scripts in version control. Do not ignore the migrations/versions folder.
- Keep sensitive information like .env files out of Git. Use .gitignore.
- For production deployment, consider building the app as an executable to avoid exposing source code.