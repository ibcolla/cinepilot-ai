import os
from dotenv import load_dotenv
import clickhouse_connect

load_dotenv('/home/ibrahima/cinepilot-ai/.env')

try:
    client = clickhouse_connect.get_client(
        host=os.getenv("CLICKHOUSE_HOST"),
        port=int(os.getenv("CLICKHOUSE_PORT", 8443)),
        username=os.getenv("CLICKHOUSE_USER", "default"),
        password=os.getenv("CLICKHOUSE_PASSWORD"),
    )
    result = client.query("SELECT 1")
    print(f"✅ ClickHouse connection successful!")
    print(f"   Result: {result.result_rows[0][0]}")
except Exception as e:
    print(f"❌ Error: {type(e).__name__}: {e}")
    import traceback
    traceback.print_exc()
