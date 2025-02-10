from airflow import DAG
from airflow.providers.postgres.operators.postgres import PostgresOperator
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import requests

default_args = {
    'owner': 'airflow',
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

def fetch_and_store_movies(api_key, pg_conn_id):
    from airflow.hooks.postgres_hook import PostgresHook
    hook = PostgresHook(postgres_conn_id=pg_conn_id)
    
    movies = []
    for page in range(1, 26):  # Fetching 500 movies (25 pages)
        url = f"https://api.themoviedb.org/3/discover/movie?include_adult=false&include_video=false&language=en-US&page={page}&sort_by=popularity.desc"
        headers = {"Authorization": f"Bearer {api_key}"}
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            movies.extend(response.json().get("results", []))
        else:
            raise Exception(f"Failed to fetch movies: {response.status_code}")
    
    insert_query = '''
        INSERT INTO tmdb_movie_discover (
            adult, backdrop_path, genre_ids, id, original_language, 
            original_title, overview, popularity, poster_path, release_date,
            title, video, vote_average, vote_count
        ) VALUES (
            %(adult)s, %(backdrop_path)s, %(genre_ids)s, %(id)s, %(original_language)s,
            %(original_title)s, %(overview)s, %(popularity)s, %(poster_path)s, %(release_date)s,
            %(title)s, %(video)s, %(vote_average)s, %(vote_count)s
        )
        ON CONFLICT (id) DO NOTHING
    '''
    for movie in movies:
        hook.run(insert_query, parameters=movie)

with DAG(
    dag_id="tmdb_movies_pipeline",
    default_args=default_args,
    description="Fetch TMDB movies and store in PostgreSQL",
    start_date=datetime(2024, 11, 28),
    schedule_interval="@once",
    catchup=False,
) as dag:

    create_table = PostgresOperator(
        task_id="create_table",
        postgres_conn_id="postgresql_conn",
        sql='''
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
        '''
    )

    fetch_and_store = PythonOperator(
        task_id="fetch_and_store",
        python_callable=fetch_and_store_movies,
        op_kwargs={
            "api_key": "{{ var.value.api_key }}",
            "pg_conn_id": "postgresql_conn",
        }
    )

    create_table >> fetch_and_store
