# Formula Backend - RISTEK Web Development Oprec

A Backend application for a Form Builder website. This project was developed as a submission for the Open Recruitment Assignment of RISTEK. 

## Tech Stack

* **Core Framework**: Django (v6.0.2).
* **API Framework**: Django REST Framework (v3.16.1).
* **Language**: Python.
* **Database**: PostgreSQL for production and SQLite (`db.sqlite3`) for local development.
* **Authentication**: JWT (JSON Web Tokens) Authentication using `djangorestframework-simplejwt`.
* **Cross-Origin Resource Sharing**: `django-cors-headers` for handling API requests from the frontend.
* **Environment Management**: `python-dotenv` for managing environment variables.

## Run Locally

Follow these steps to set up and run the development server on your local machine:

### Prerequisites
Make sure you have **Python** and a package manager like **pip** installed on your system.

### Steps

1.  **Clone the Repository**:
    If you haven't already, clone this repository to your local machine.
    ```bash
    git clone <repository-url>
    cd formula-backend
    ```

2.  **Install Dependencies**:
    Run the following command to install all required Python modules:
    ```bash
    pip install -r requirements.txt
    ```

3.  **Apply Migrations**:
    Set up the local SQLite database by running the initial migrations:
    ```bash
    python manage.py migrate
    ```

4.  **Run the Development Server**:
    Start the local Django server by running:
    ```bash
    python manage.py runserver
    ```
