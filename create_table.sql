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
