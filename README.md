# Formula Backend - RISTEK Web Development Oprec

A Backend application for a Form Builder website. This project was developed as a submission for the Open Recruitment Assignment of RISTEK. 

## Tech Stack

* **Core Framework**: Django (v6.0.2).
* **API Framework**: Django REST Framework (v3.16.1).
* **Language**: Python.
* **Database**: PostgreSQL for production and SQLite (`db.sqlite3`) for local development.
* **Authentication**: JWT (JSON Web Tokens).


## Run Locally

Follow these steps to set up and run the development server on your local machine:

### Prerequisites
Make sure you have **Python** and a package manager like **pip** installed on your system.

### Steps

1.  **Clone the Repository**:
    If you haven't already, clone this repository to your local machine.
    ```bash
    git clone https://github.com/chefkeenan/formula-backend
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
### API Endpoints

Authentication
- Register: POST /api/auth/register/
- Login : POST /api/token/
- Refresh Token: POST /api/token/refresh/

Forms
- List All Forms: GET /api/forms/
- Create Form: POST /api/forms/
- Form Detail: GET /api/forms/<uuid:id>/
- Update Form (Full): PUT /api/forms/<uuid:id>/
- Update Form (Partial): PATCH /api/forms/<uuid:id>/
- Delete Form: DELETE /api/forms/<uuid:id>/

Submissions
- Submit Response: POST /api/forms/submissions/
- View All Submissions: GET /api/forms/<uuid:form_id>/submissions/

