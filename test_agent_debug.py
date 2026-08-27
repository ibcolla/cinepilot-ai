import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)

print("Testing Gemini directly with MCP context...\n")

mcp_context = """You have access to ClickHouse production database via MCP.
Query the cinepilot database for production_decisions table.
Example: SELECT * FROM cinepilot.production_decisions WHERE scene_id='SC12'"""

request = f"""{mcp_context}

Scene 12 Continuity Issue:
- Expected: Blue jacket
- Observed (Take 2): Black jacket
- Expected: Coffee cup on desk
- Observed (Take 2): Coffee cup missing

Analyze these issues and provide continuity recommendations."""

print("Sending request to Gemini...")
try:
    response = client.models.generate_content(
        model="gemini-3.6-flash",
        contents=[{"role": "user", "parts": [{"text": request}]}],
    )
    
    result = response.text if hasattr(response, "text") else str(response)
    print(f"\n✅ Gemini Response ({len(result)} chars):\n")
    print(result)
    
except Exception as e:
    print(f"❌ Error: {type(e).__name__}: {e}")
    import traceback
    traceback.print_exc()
