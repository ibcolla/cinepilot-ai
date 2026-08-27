import os
from dotenv import load_dotenv

load_dotenv()

print("Testing mcp-clickhouse with correct credentials...\n")

# Set MCP environment
os.environ['CLICKHOUSE_HOST'] = os.getenv("CLICKHOUSE_HOST")
os.environ['CLICKHOUSE_PORT'] = os.getenv("CLICKHOUSE_PORT")
os.environ['CLICKHOUSE_USER'] = os.getenv("CLICKHOUSE_USER")
os.environ['CLICKHOUSE_PASSWORD'] = os.getenv("CLICKHOUSE_PASSWORD")

try:
    # Import and test mcp_clickhouse
    from mcp_clickhouse.tools import run_query
    
    result = run_query("SELECT COUNT(*) as count FROM cinepilot.scenes WHERE scene_id='SC12'")
    print(f"✅ MCP ClickHouse Query Successful!")
    print(f"   Result: {result}")
    
except Exception as e:
    print(f"❌ Error: {type(e).__name__}: {e}")
    import traceback
    traceback.print_exc()
