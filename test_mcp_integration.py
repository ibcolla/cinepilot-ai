import os
from dotenv import load_dotenv
from google.adk.tools.mcp_tool.mcp_toolset import McpToolset, StdioServerParameters

load_dotenv()

print("Testing McpToolset with mcp-clickhouse...\n")

# Set MCP environment
os.environ['CLICKHOUSE_HOST'] = os.getenv("CLICKHOUSE_HOST")
os.environ['CLICKHOUSE_PORT'] = os.getenv("CLICKHOUSE_PORT")
os.environ['CLICKHOUSE_USER'] = os.getenv("CLICKHOUSE_USER")
os.environ['CLICKHOUSE_PASSWORD'] = os.getenv("CLICKHOUSE_PASSWORD")

try:
    # Create McpToolset (new API)
    toolset = McpToolset(
        connection_params=StdioServerParameters(
            command="python",
            args=["-m", "mcp_clickhouse"],
        ),
    )
    
    print(f"✅ McpToolset created successfully!")
    print(f"   Available tools: {list(toolset.tools.keys())}")
    
    # Check for run_query tool
    if 'run_query' in toolset.tools:
        print(f"\n✅ run_query tool available")
    else:
        print(f"❌ run_query tool not found")
    
except Exception as e:
    print(f"❌ Error: {type(e).__name__}: {e}")
    import traceback
    traceback.print_exc()
