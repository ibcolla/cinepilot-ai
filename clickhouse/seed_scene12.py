"""
Admin script to seed Scene 12 test data into ClickHouse.

Uses clickhouse-connect directly (admin only, NOT agent path).
"""

import os
import logging
from dotenv import load_dotenv
import clickhouse_connect

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

load_dotenv()


def get_client():
    """Create ClickHouse client"""
    return clickhouse_connect.get_client(
        host=os.getenv("CLICKHOUSE_HOST"),
        port=int(os.getenv("CLICKHOUSE_PORT", 8443)),
        username=os.getenv("CLICKHOUSE_USER", "default"),
        password=os.getenv("CLICKHOUSE_PASSWORD"),
    )


def create_schema():
    """Create production intelligence schema"""
    client = get_client()
    logger.info("Creating ClickHouse schema...")
    
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
    
    client.command("""
    CREATE TABLE IF NOT EXISTS cinepilot.takes (
        take_id String,
        scene_id String,
        movie_id String,
        take_number Int32,
        video_reference String,
        created_at DateTime DEFAULT now()
    ) ENGINE = MergeTree()
    ORDER BY (movie_id, scene_id, take_number)
    """)
    
    client.command("""
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
    ORDER BY (movie_id, scene_id, detected_at)
    """)
    
    client.command("""
    CREATE TABLE IF NOT EXISTS cinepilot.production_decisions (
        decision_id String,
        scene_id String,
        movie_id String,
        approved_take String,
        reason String,
        approved_at DateTime,
        created_at DateTime DEFAULT now()
    ) ENGINE = MergeTree()
    ORDER BY (movie_id, scene_id, approved_at)
    """)
    
    logger.info("✅ Schema created")


def seed_scene12_data():
    """Seed Scene 12 test data"""
    client = get_client()
    logger.info("Seeding Scene 12 test data...")
    
    client.insert("cinepilot.scenes", [{
        "scene_id": "SC12",
        "movie_id": "movie_001",
        "title": "Office Arrival",
        "location": "Modern Office",
        "characters": ["Daniel", "Sarah"],
        "props": ["Coffee cup", "Blue jacket", "Laptop", "Phone"],
        "created_at": "2026-08-21 12:00:00",
    }])
    
    client.insert("cinepilot.takes", [
        {
            "take_id": "SC12_T001",
            "scene_id": "SC12",
            "movie_id": "movie_001",
            "take_number": 1,
            "video_reference": "video/scene_12/take_01.mp4",
            "created_at": "2026-08-21 12:00:00",
        },
        {
            "take_id": "SC12_T002",
            "scene_id": "SC12",
            "movie_id": "movie_001",
            "take_number": 2,
            "video_reference": "video/scene_12/take_02.mp4",
            "created_at": "2026-08-21 12:00:00",
        },
    ])
    
    client.insert("cinepilot.continuity_issues", [
        {
            "issue_id": "SC12_ISSUE_001",
            "scene_id": "SC12",
            "take_id": "SC12_T002",
            "movie_id": "movie_001",
            "category": "costume",
            "description": "Black jacket instead of approved blue",
            "severity": "critical",
            "confidence": 0.96,
            "detected_at": "2026-08-21 12:00:00",
        },
        {
            "issue_id": "SC12_ISSUE_002",
            "scene_id": "SC12",
            "take_id": "SC12_T002",
            "movie_id": "movie_001",
            "category": "prop",
            "description": "Coffee cup missing",
            "severity": "high",
            "confidence": 0.91,
            "detected_at": "2026-08-21 12:00:00",
        },
    ])
    
    client.insert("cinepilot.production_decisions", [{
        "decision_id": "SC12_DECISION_001",
        "scene_id": "SC12",
        "movie_id": "movie_001",
        "approved_take": "SC12_T001",
        "reason": "Take 1 correct: blue jacket + coffee cup",
        "approved_at": "2026-08-21 12:00:00",
        "created_at": "2026-08-21 12:00:00",
    }])
    
    logger.info("✅ Scene 12 data seeded")


def verify_data():
    """Verify data was inserted"""
    client = get_client()
    logger.info("Verifying data...")
    
    scenes = client.query("SELECT COUNT(*) FROM cinepilot.scenes WHERE scene_id='SC12'")
    logger.info(f"  Scenes: {scenes.result_rows[0][0]}")
    
    decisions = client.query("SELECT COUNT(*) FROM cinepilot.production_decisions WHERE scene_id='SC12'")
    logger.info(f"  Production Decisions: {decisions.result_rows[0][0]}")
    
    issues = client.query("SELECT COUNT(*) FROM cinepilot.continuity_issues WHERE scene_id='SC12'")
    logger.info(f"  Continuity Issues: {issues.result_rows[0][0]}")
    
    logger.info("✅ Data verified")


if __name__ == "__main__":
    try:
        create_schema()
        seed_scene12_data()
        verify_data()
        logger.info("\n✅ Scene 12 initialization complete\n")
    except Exception as e:
        logger.error(f"Error: {e}", exc_info=True)
        raise
