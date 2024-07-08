Here is an updated `README.md` file with a focus on setup instructions and without creating a superuser:

```markdown
# Journal Application

This is a Django application for managing journal entries with PostgreSQL as the database.

## Prerequisites

- Python 3.6+
- PostgreSQL

## Setup

### Clone the Repository

First, clone the repository to your local machine:

```bash
git clone https://github.com/morachake/journal.git
cd journal
```

### Create a Virtual Environment

Create and activate a virtual environment:

```bash
python -m venv env
source env/bin/activate  # On Windows use `env\Scripts\activate`
```

### Install Dependencies

Install the required dependencies using `pip`:

```bash
pip install -r requirements.txt
```

### Configure Environment Variables

Create a `.env` file in the project root. You can use the provided `.env.example` as a template. Copy it and rename it to `.env`:

```bash
cp .env.example .env
```

Edit the `.env` file to match your PostgreSQL configuration:

```plaintext
DJANGO_DEBUG=True
DJANGO_ALLOWED_HOSTS=localhost,127.0.0.1
POSTGRES_DB=journal
POSTGRES_USER=postgres
POSTGRES_PASSWORD=yourpassword
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
```

Replace `yourpassword` with your actual PostgreSQL password.

### Set Up the Database

1. Ensure PostgreSQL is installed and running on your machine.
2. Create the PostgreSQL database:

```bash
psql -U postgres
CREATE DATABASE journal;
```

### Apply Migrations

Apply the initial database migrations:

```bash
python manage.py makemigrations
python manage.py migrate
```

### Run the Development Server

Start the Django development server:

```bash
python manage.py runserver
```

Access the application at `http://localhost:8000`.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Troubleshooting

### Common Issues

1. **Database Connection Issues**:
   - Ensure PostgreSQL is running and the credentials in your `.env` file are correct.
   - Verify that the database host is set to `localhost` if running locally.

2. **Missing Dependencies**:
   - Run `pip install -r requirements.txt` to install any missing dependencies.

3. **Migrations Not Applied**:
   - Run `python manage.py makemigrations` and `python manage.py migrate` to apply migrations.

If you encounter any issues, please refer to the Django and PostgreSQL documentation or seek help from the community.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request for any improvements or bug fixes.
```

### `.env.example` File

Create an `.env.example` file in the project root to serve as a template for users:

```plaintext
DJANGO_DEBUG=True
DJANGO_ALLOWED_HOSTS=localhost,127.0.0.1
POSTGRES_DB=journal
POSTGRES_USER=postgres
POSTGRES_PASSWORD=yourpassword
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
```

Replace `yourpassword` with a placeholder to remind users to enter their actual password.

