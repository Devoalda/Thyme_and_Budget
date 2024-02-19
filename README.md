# Backend

This is the backend of our application, built with Django. It provides a set of RESTful APIs for managing recipes.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

- Python 3.8 or higher
- pip

### Installation

1. Clone the repository and navigate to the backend directory:

    ```bash
    git clone <repo-url>
    cd Backend
    ```

2. (Optional) Create a virtual environment and activate it:

    ```bash
    python -m venv venv
    source venv/bin/activate
    ```

    For Windows:

    ```bash
    venv\Scripts\activate
    ```

3. Install the required libraries:

    ```bash
    pip install -r requirements.txt
    ```
   
3. (Optional) Create PostgresSQL database:

   For macOS:
   ```bash
    brew install postgresql
    brew services start postgresql
   ```
   ```bash
    psql postgres
    CREATE DATABASE thyme_and_budget;
    CREATE ROLE thyme_and_budget_user WITH LOGIN PASSWORD 'password';
    GRANT ALL ON DATABASE thyme_and_budget TO thyme_and_budget_user;
   ```

4. Run migrations:

    ```bash
    python manage.py makemigrations
    python manage.py migrate
    ```

5. Run the seed script to populate the database with some initial user and food item data (optional):

    ```bash
   python manage.py seed_users 5
    python manage.py seed_food_items 5
    ```

6. Start the server:

    ```bash
    python manage.py runserver
    ```

## API Endpoints

For a detailed list of all API endpoints, please refer to the [API Documentation](API.md).

## Testing

To run the tests:

```bash
python manage.py test
```