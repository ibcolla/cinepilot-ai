import os
from dotenv import load_dotenv
import clickhouse_connect

load_dotenv()

client = clickhouse_connect.get_client(
    host=os.getenv("CLICKHOUSE_HOST"),
    port=int(os.getenv("CLICKHOUSE_PORT", 8443)),
    username=os.getenv("CLICKHOUSE_USER", "default"),
    password=os.getenv("CLICKHOUSE_PASSWORD"),
)

print("Seeding production_decisions for Scene 12...")

client.command("""
INSERT INTO cinepilot.production_decisions VALUES
('SC12_DECISION_001', 'SC12', 'movie_001', 'SC12_T001', 'Take 1: Daniel in blue jacket + coffee cup present - APPROVED', '2026-08-21 12:00:00', '2026-08-21 12:00:00')
""")

print("✅ Production decision seeded!")

# Verify
result = client.query("SELECT COUNT(*) FROM cinepilot.production_decisions WHERE scene_id='SC12'")
print(f"   Verified: {result.result_rows[0][0]} decision(s) in database")
