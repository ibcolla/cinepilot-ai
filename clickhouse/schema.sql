-- CinePilot Production Intelligence Schema

CREATE DATABASE IF NOT EXISTS cinepilot;

CREATE TABLE IF NOT EXISTS cinepilot.scenes (
    scene_id String,
    movie_id String,
    title String,
    location String,
    time_of_day String,
    characters Array(String),
    props Array(String),
    created_at DateTime DEFAULT now()
) ENGINE = MergeTree()
ORDER BY (movie_id, scene_id);

CREATE TABLE IF NOT EXISTS cinepilot.takes (
    take_id String,
    scene_id String,
    movie_id String,
    take_number Int32,
    video_reference String,
    created_at DateTime DEFAULT now()
) ENGINE = MergeTree()
ORDER BY (movie_id, scene_id, take_number);

CREATE TABLE IF NOT EXISTS cinepilot.continuity_issues (
    issue_id String,
    scene_id String,
    take_id String,
    movie_id String,
    category String,
    description String,
    severity String,
    confidence Float32,
    detected_at DateTime DEFAULT now()
) ENGINE = MergeTree()
ORDER BY (movie_id, scene_id, detected_at);

CREATE TABLE IF NOT EXISTS cinepilot.production_decisions (
    decision_id String,
    scene_id String,
    movie_id String,
    approved_take String,
    reason String,
    approved_at DateTime,
    created_at DateTime DEFAULT now()
) ENGINE = MergeTree()
ORDER BY (movie_id, scene_id, approved_at);