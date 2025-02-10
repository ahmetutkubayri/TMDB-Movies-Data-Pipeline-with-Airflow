# TMDB Movies Data Pipeline with Airflow 🎬

This project sets up an **ETL pipeline** using **Apache Airflow** and **PostgreSQL** to ingest at least **500 random movies** from [TMDB Discover API](https://developer.themoviedb.org/reference/discover-movie). The movies are stored in the **traindb database** in the `tmdb_movie_discover` table.

## 📌 Business Requirements
- **Fetch at least 500 movies** using **TMDB API**.
- Store movies in the **`traindb.tmdb_movie_discover`** table.
- **Schedule:** **Run once (`@once`)**.
- **Airflow & PostgreSQL Integration**.

## 📁 Repository Structure
- `dags/tmdb_movies_pipeline.py` → **Airflow DAG for ETL process**.
- `sql/create_table.sql` → **DDL script to create the movies table**.
- `.env` → **Environment variables (DO NOT expose API keys in the code).**

---

## 🏗️ PostgreSQL Table Schema

```sql
CREATE TABLE IF NOT EXISTS tmdb_movie_discover (
    adult BOOLEAN,
    backdrop_path TEXT,
    genre_ids INTEGER[],
    id BIGINT PRIMARY KEY,
    original_language TEXT,
    original_title TEXT,
    overview TEXT,
    popularity DOUBLE PRECISION,
    poster_path TEXT,
    release_date TEXT,
    title TEXT,
    video BOOLEAN,
    vote_average DOUBLE PRECISION,
    vote_count INTEGER
);
```

---

## 🚀 Setting Up Airflow & Running the DAG

### **1. Configure API Key in Airflow**
- Go to **Airflow UI > Admin > Variables**.
- Add a new variable:
  - **Key:** `api_key`
  - **Value:** `<your_tmdb_api_key>`

### **2. Configure PostgreSQL Connection in Airflow**
- Go to **Airflow UI > Admin > Connections**.
- Add a new connection:
  - **Conn ID:** `postgresql_conn`
  - **Conn Type:** `Postgres`
  - **Host:** `postgres`
  - **Schema:** `traindb`
  - **Login:** `airflow`
  - **Password:** `airflow`
  - **Port:** `5432`

### **3. Deploy & Run DAG**

1. **Copy the DAG file into Airflow:**
   ```bash
   docker cp tmdb_movies_pipeline.py airflow-webserver:/opt/airflow/dags/
   ```

2. **Trigger DAG in Airflow UI:**
   - Open **Airflow Web UI** (`http://localhost:8080`).
   - Locate `tmdb_movies_pipeline` DAG.
   - Click **Trigger DAG**.

3. **Check Logs:** Monitor logs in **Airflow UI** or using:
   ```bash
   docker logs airflow-webserver
   ```

---

## 📌 Summary
- **Airflow DAG** fetches 500+ movies and stores them in PostgreSQL.
- **`tmdb_movie_discover` table** contains structured movie data.
- **No sensitive data (API keys, passwords) exposed in the code.**

