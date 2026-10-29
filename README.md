## Application Architecture and Python File Responsibilities

### 1. Project Overview

The Movie Intelligence Platform is a Python-based movie analytics application that combines interactive data visualization, REST API services, database management, and user interaction tracking.

The application uses the TMDB 5000 Movies and Credits datasets as its initial data source. The CSV files are processed and imported into a database, where the FastAPI backend provides structured access to movie records and analytical results.

The platform consists of two main consumers:

- **Movie Analytics Dashboard:** Provides movie exploration, statistical analysis, financial insights, comparisons, data management, and engagement analytics.
- **Partner Recommendation Application:** Consumes the same API to access movie data and record user interactions. Recommendation algorithm logic remains in the partner application.

Both applications can work with the same movie records and interaction data through a shared API, avoiding separate movie catalogues.

### 2. System Architecture

```text
              TMDB Movies and Credits CSV
                         |
                         v
                 data_loader.py
              Data parsing and cleaning
                         |
                         v
                    manage.py
                  CSV import
                         |
                         v
                 Database Layer
              database.py + models.py
                         |
                         v
                 FastAPI Application
                     main.py
                         |
             +-----------+-----------+
             |                       |
             v                       v
         api.py                 interactions.py
     Movie and analytics       User activity and
          endpoints            recommendation events
             |                       |
             +-----------+-----------+
                         |
             +-----------+-----------+
             |                       |
             v                       v
       analytics.py          auth.py / schemas.py
     Metrics and rankings   Authentication and
                            input validation
             |                       |
             +-----------+-----------+
                         |
                         v
                   JSON Responses
                         |
              +----------+----------+
              |                     |
              v                     v
       frontend.py             Partner Client
     Analytics Dashboard      partner_client.py
              |
              v
        Browser Interface
```

**Request-response flow:**

1. The user opens the dashboard, which is served by the FastAPI application.
2. The frontend JavaScript sends HTTP requests to the relevant API endpoints.
3. The API layer validates the request and invokes the required database or analytics operations.
4. The database layer retrieves or updates records.
5. The analytics layer calculates the requested metrics when required.
6. FastAPI returns the result as JSON.
7. The frontend renders the response as summary cards, charts, tables, or movie details.

Not every request uses every module. For example, a simple movie-detail request may access the database directly, while an analytics request may also invoke `analytics.py`.

### 3. Dashboard Modules

The dashboard provides the following analytical and operational capabilities:

| Module | Purpose |
|---|---|
| Overview | Displays high-level catalogue statistics, summary metrics, and analytical charts. |
| Movie Explorer | Supports movie search, filtering, sorting, and browsing. |
| Industry and Genre Analytics | Examines genre distribution, release trends, languages, production companies, countries, directors, and related patterns. |
| Financial Insights | Compares movie budgets and revenues and calculates estimated profit and ROI where data is available. |
| Ratings and Popularity | Analyzes audience ratings, vote counts, popularity, and rating distributions. |
| Movie Comparison | Compares two to four selected movies and presents their differences. |
| User Engagement | Analyzes recorded ratings, likes, watchlists, recommendation impressions, clicks, and feedback. |
| Data Management | Provides authorized editing, data-quality information, and CSV exports. |

The available insights depend on the imported dataset and recorded user activity. Financial calculations use the available budget and revenue values; they should not be interpreted as audited profitability.

### 4. Python File Responsibilities

The application uses modular Python files to separate configuration, data access, analytics, API handling, authentication, and frontend rendering.

| File | Responsibility |
|---|---|
| `config.py` | Loads application configuration and environment variables, including database settings and other operational options. |
| `data_loader.py` | Reads the movie and credits CSV files, parses structured fields, combines related records, and prepares the data for database import. |
| `models.py` | Defines SQLAlchemy database models for movies, editors, application users, interactions, and reviews. |
| `database.py` | Creates database connections and sessions, retrieves movie records, provides analytical data access, and manages database-related operations. |
| `analytics.py` | Implements reusable analytical calculations, including summary metrics, genre statistics, rating distributions, financial calculations, rankings, and movie comparisons. |
| `schemas.py` | Defines Pydantic request and response schemas and validates incoming data. |
| `auth.py` | Implements password hashing, token creation and verification, user authentication, and editor authorization. |
| `api.py` | Defines REST API endpoints for movie retrieval, search, analytics, comparisons, data quality, editing, and CSV exports. |
| `interactions.py` | Implements endpoints for user ratings, likes, dislikes, watchlists, recommendation events, and feedback. |
| `frontend.py` | Contains the dashboard's HTML, CSS, and JavaScript and handles the browser-side interface and API interactions. |
| `main.py` | Creates the FastAPI application, configures middleware, registers routers, handles startup, and serves the dashboard. |
| `manage.py` | Provides command-line operations for database initialization, CSV import, editor creation, schema upgrades, and optional poster enrichment. |
| `partner_client.py` | Provides an example Python client for accessing the shared API from a partner application. |

### 5. Supporting Files and Directories

| File or directory | Purpose |
|---|---|
| `requirements.txt` | Lists the Python dependencies required to run the application. |
| `README.md` | Documents architecture, setup, database design, API usage, testing, deployment, and troubleshooting. |
| `render.yaml` | Defines the Render service deployment configuration. |
| `.env.example` | Provides example environment variable names and configuration settings. |
| `.gitignore` | Prevents local environments, secrets, and other excluded files from being committed to Git. |
| `data/` | Contains the source movie and credits CSV datasets. |
| `tests/` | Contains automated tests for API behaviour, database operations, data processing, validation, and platform functionality. |

### 6. Database Design

The application defines its main entities through SQLAlchemy models.

| Table | Description |
|---|---|
| `movies` | Stores movie metadata, including title, release date, genres, ratings, vote counts, popularity, budget, revenue, cast, crew, and production information. |
| `editors` | Stores editor account information and password hashes. |
| `app_users` | Stores registered application user accounts. |
| `interactions` | Stores user ratings, reactions, watchlist state, and recommendation events. |
| `reviews` | Stores review records associated with movies. |

Movie records use the TMDB movie ID as their primary key. Interactions reference movie records and user identities.

The database is the operational source of truth for the application. CSV files provide the initial dataset and can also serve as a source for re-importing data. Editing a movie through the application updates the database rather than rewriting the original CSV files.

The application supports SQLite for local development and PostgreSQL for a shared hosted deployment. The actual database used depends on the configured `DATABASE_URL`.

### 7. API and Application Integration

FastAPI exposes REST endpoints for accessing movie records, retrieving analytics, comparing movies, managing authorized edits, and recording user activity.

The API provides a common interface for both the analytics dashboard and the partner recommendation application.

Example endpoints include:

- `GET /api/health` — checks application and database status.
- `GET /api/movies` — retrieves movie records with supported filtering and pagination.
- `GET /api/movies/{id}` — retrieves an individual movie.
- `GET /api/analytics/summary` — retrieves summary analytics.
- `GET /api/analytics/genres` — retrieves genre statistics.
- `GET /api/analytics/financials` — retrieves financial metrics.
- `GET /api/analytics/compare?ids=1,2` — compares selected movies.
- `POST /api/interactions` — records supported user interactions.

The complete endpoint definitions, parameters, request schemas, and access rules are documented in the API contract section of this README. Interactive API documentation is available at `/docs` when the application is running.

### 8. Analytics Methodology

The analytics layer uses Pandas and NumPy to process structured movie data and calculate metrics.

Examples include:

- **Average rating:** Mean of available movie ratings.
- **Genre distribution:** Counts or groups movies by genre.
- **Release-year trends:** Groups movie records by release year.
- **Estimated profit:** Revenue minus budget.
- **Estimated ROI:** `(Revenue - Budget) / Budget * 100`, provided the budget is known and positive.
- **Movie ranking:** Orders records according to rating, popularity, revenue, votes, or other supported fields.
- **Recommendation click-through rate:** Recorded recommendation clicks divided by recorded impressions, when impressions are greater than zero.

Unknown budget, revenue, runtime, and rating values must not be interpreted as genuine zero values. Financial and engagement metrics should be calculated only when their required inputs are available.

### 9. Security and Data Integrity

The application includes several mechanisms for protecting data and maintaining consistency:

- Passwords are stored as scrypt hashes rather than plaintext.
- Signed bearer tokens are used for authenticated API requests.
- Editor-only operations are protected by authorization checks.
- Pydantic schemas validate incoming request data.
- Movie metadata updates are restricted to explicitly permitted fields.
- User interactions are stored separately from the original TMDB ratings.
- Database constraints and indexes support data integrity and query performance.
- Environment variables are used for deployment configuration and secrets.

Production deployments should use HTTPS, a strong secret key, an appropriately restricted CORS configuration, and a secured database connection. Additional operational controls may be needed before the application is used with real users.

### 10. Running the Application Locally

From the project root, create and activate a virtual environment:

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

Install dependencies:

```powershell
python -m pip install -r requirements.txt
```

Initialize the database and import the dataset:

```powershell
python manage.py init-db
python manage.py import-csv
```

Optionally create an editor account:

```powershell
python manage.py create-editor alice
```

Start the FastAPI server:

```powershell
python -m uvicorn main:app --reload
```

Open the dashboard at `http://127.0.0.1:8000` and interactive API documentation at `http://127.0.0.1:8000/docs`.

To verify that the dataset was imported, visit `http://127.0.0.1:8000/api/health`. A successful setup should report a connected database and a nonzero movie count.

For more detailed setup, cloud deployment, backup, testing, and troubleshooting instructions, refer to the corresponding sections of this README.
