import os
from dotenv import load_dotenv
import clickhouse_connect

load_dotenv()

def get_client():
    return clickhouse_connect.get_client(
        host=os.getenv("CLICKHOUSE_HOST"),
        port=int(os.getenv("CLICKHOUSE_PORT", 8443)),
        username=os.getenv("CLICKHOUSE_USER", "default"),
        password=os.getenv("CLICKHOUSE_PASSWORD"),
    )

client = get_client()

print("Creating schema...")
client.command("CREATE DATABASE IF NOT EXISTS cinepilot")

client.command("""
CREATE TABLE IF NOT EXISTS cinepilot.scenes (
    scene_id String,
    movie_id String,
    title String,
    location String,
    characters Array(String),
    props Array(String),
    created_at DateTime DEFAULT now()
) ENGINE = MergeTree()
ORDER BY (movie_id, scene_id)
""")

print("Seeding Scene 12...")
client.command("""
INSERT INTO cinepilot.scenes VALUES
('SC12', 'movie_001', 'Office Arrival', 'Modern Office', ['Daniel', 'Sarah'], ['Coffee cup', 'Blue jacket', 'Laptop', 'Phone'], '2026-08-21 12:00:00')
""")

print("✅ Scene 12 seeded successfully!")
