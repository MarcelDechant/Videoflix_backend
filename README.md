# Videoflix Backend

Videoflix is a backend service designed for a video streaming platform, built with Django. It offers a range of features including user registration, password recovery, video management, and additional functionalities to support video streaming operations.

## Features

- **User Management:** Registration, login, and password reset.
- **Video Management:** Upload, management, and retrieval of video content.
- **Background Tasks:** Background processes for tasks like video encoding via RQWorker.
- **Security:** Authentication and authorization using JWT (JSON Web Tokens).
- **Email Notifications:** Send emails for registration and password reset.

## Prerequisites

To run this backend locally, make sure you have the following tools installed:

- [Python 3.9+](https://www.python.org/downloads/)
- [PostgreSQL](https://www.postgresql.org/download/)
- [Redis](https://redis.io/download)
- [FFmpeg](https://ffmpeg.org/download.html)
- [Git](https://git-scm.com/)
- [Virtualenv](https://virtualenv.pypa.io/en/latest/)

## Installation

1. **Clone the Repository:**
   ```bash
   git clone https://github.com/MarcelDechant/videoflix-backend.git
   cd videoflix-backend

2. **Create and activate a virtual environment:**
   If you don't have virtualenv installed, you can install it with pip install virtualenv.
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   
3. **Install the dependencies**
   ```bash
   pip install -r requirements.txt

4. **Set up PostgreSQL:**
   Install PostgreSQL and create a database for the project.
   Create a PostgreSQL user and database. You can do this by running the following in psql:
   ```sql
   CREATE DATABASE videoflix;
   CREATE USER videoflix_user WITH PASSWORD 'yourpassword';
   ALTER ROLE videoflix_user SET client_encoding TO 'utf8';
   ALTER ROLE videoflix_user SET default_transaction_isolation TO 'read committed';
   ALTER ROLE videoflix_user SET timezone TO 'UTC';
   GRANT ALL PRIVILEGES ON DATABASE videoflix TO videoflix_user;

5. **Set up the environment variables:**  
   Create a `.env` file in the root of the project and add the following environment variables:  
   
   ```ini
   # Django settings
   SECRET_KEY=your-secret-key                      # Replace with your Django secret key
   DEBUG=True                                      # Set to False in production
   ALLOWED_HOSTS=http://localhost:4200,127.0.0.1,localhost  # Allowed hosts

   # Database settings
   DATABASE_ENGINE=django.db.backends.sqlite3      # Database engine (SQLite as default)
   DATABASE_NAME=db.sqlite3                        # SQLite database file

   # PostgreSQL settings (if using PostgreSQL instead of SQLite)
   DATABASE_postgres_NAME= videoflix                # Name of the PostgreSQL database
   DATABASE_postgres_USER= Username                # PostgreSQL username
   DATABASE_postgres_PASSWORD=your-secure-password # PostgreSQL password
   DATABASE_postgres_HOST=localhost                # PostgreSQL host
   DATABASE_postgres_PORT=5432                     # Default PostgreSQL port

   # Redis settings for background task queue (RQWorker)
   RQ_HOST=172.29.64.1                             # Redis server host
   RQ_PORT=6379                                    # Redis server port
   RQ_DB=0                                         # Redis database index
   RQ_PASSWORD=password                           # Password for Redis (if required)
   RQ_DEFAULT_TIMEOUT=600                          # Default task timeout (seconds)

   # CORS settings
   CORS_ALLOWED_ORIGINS=http://localhost:4200      # Allowed origins for CORS

   # Cache settings
   CACHE_BACKEND=django_redis.cache.RedisCache     # Cache backend
   CACHE_LOCATION=redis://localhost:6379/1         # Redis cache location
   CACHE_PASSWORD=password                         # Cache password (if applicable)
   CACHE_KEY_PREFIX=videoflix                      # Prefix for cache keys
   CACHE_TTL=1800                                  # Cache time-to-live (seconds)

   # Email settings for sending emails
   EMAIL_BACKEND=django.core.mail.backends.console.EmailBackend  # Email backend
   EMAIL_HOST=smtp.dein-email-server.de            # SMTP server address
   EMAIL_PORT=587                                  # SMTP port (587 for TLS)
   EMAIL_USE_TLS=True                              # Enable TLS
   EMAIL_HOST_USER=dein-benutzername@deinedomain.com  # Email username
   EMAIL_HOST_PASSWORD=dein-passwort               # Email password

   # Media settings
   MEDIA_ROOT=media                                # Root directory for media files
   MEDIA_URL=/media/                               # URL path for media files

   # JWT authentication settings
   SIMPLE_JWT_ACCESS_TOKEN_LIFETIME=300           # Access token lifetime in seconds
   SIMPLE_JWT_REFRESH_TOKEN_LIFETIME=86400        # Refresh token lifetime in seconds

6. **Install FFmpeg:**
   Install FFmpeg for video processing (for example, for encoding videos). Follow the installation guide for your operating system.

7. **Migrate the database:**
   Run the migrations to set up the database schema:
   ```bash
   python manage.py makemigrations
   python manage.py migrate

8. **Create a Superuser:**
   To create an admin superuser, run the following command:
   ```bash
   python manage.py createsuperuser

   Follow the prompts to create the superuser.

9. **Start the Redis server**
   If Redis is not running, start it by running:
    ```bash
    redis-server

10. **Start RQ Worker under WSL**

If you are using Windows, you need to run the RQ Worker on WSL (Windows Subsystem for Linux). Additionally you have to install the dependencies from the `requirements_lin.txt`.

1. Install the dependencies in WSL:
   ```bash
   pip install -r requirements_lin.txt

2. Start the RQ Worker under WSL
    ```bash
    python manage.py rqworker

11. **Start backend server**

    After all previous steps are completed, you can now start the backend server. To do this, use the following command:

    ```bash
    python manage.py runserver

12. **Add videos via admin panel**

    To add videos, you must first log in via the admin panel.

    1. Make sure the backend server is running (`python manage.py runserver`).
    2. Go to `http://127.0.0.1:8000/admin` in the browser.
    3. Sign in with the superuser account you created previously.
    4. In the admin panel you can now add videos using the “Video” model. To do this, click on “Videos” and add your videos.

   Now you can manage your videos and make them available to users!