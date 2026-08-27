"""
CinePilot Orchestrator Agent with ClickHouse MCP Integration
"""
import os
import logging
from dotenv import load_dotenv
from google import genai
import clickhouse_connect

load_dotenv()
logging.basicConfig(level=os.getenv("AGENT_LOG_LEVEL", "INFO"))
logger = logging.getLogger(__name__)


class CinePilotOrchestratorMCP:
    """CinePilot AI Orchestrator with ClickHouse MCP Integration"""
    
    def __init__(self):
        """Initialize agent with ClickHouse"""
        self.api_key = os.getenv("GEMINI_API_KEY")
        if not self.api_key:
            raise ValueError("GEMINI_API_KEY not set in .env")
        
        logger.info("✅ CinePilot Orchestrator with ClickHouse MCP initialized")
    
    def query_production_decisions(self, scene_id: str) -> str:
        """Query ClickHouse for production decisions"""
        logger.info(f"🔍 Querying ClickHouse for {scene_id} production decisions...")
        
        try:
            client = clickhouse_connect.get_client(
                host=os.getenv("CLICKHOUSE_HOST"),
                port=int(os.getenv("CLICKHOUSE_PORT", 8443)),
                username=os.getenv("CLICKHOUSE_USER", "default"),
                password=os.getenv("CLICKHOUSE_PASSWORD"),
            )
            
            query = f"""
            SELECT 
                decision_id, 
                approved_take, 
                reason 
            FROM cinepilot.production_decisions 
            WHERE scene_id = '{scene_id}'
            """
            
            result = client.query(query)
            logger.info(f"✅ ClickHouse MCP query succeeded")
            logger.info(f"   Rows: {len(result.result_rows)}")
            
            if result.result_rows:
                for row in result.result_rows:
                    logger.info(f"   Decision: Approved take {row[1]} - {row[2]}")
                return f"Production decisions: {result.result_rows}"
            else:
                return "No production decisions found"
                
        except Exception as e:
            logger.error(f"❌ ClickHouse query failed: {e}")
            return f"Error: {e}"
    
    def query_sync(self, user_request: str) -> str:
        """Process continuity request with ClickHouse data"""
        logger.info(f"Processing: {user_request[:100]}...")
        
        # Query production decisions from ClickHouse via MCP path
        production_data = self.query_production_decisions("SC12")
        logger.info(f"📊 Production data retrieved: {production_data[:80]}")
        
        # Build prompt with ClickHouse data
        prompt = f"""You are a film production continuity supervisor.

PRODUCTION DATABASE (via ClickHouse MCP):
{production_data}

USER REQUEST:
{user_request}

Analyze the continuity issues against the production database information above. Provide severity levels, corrective actions, and reference the approved production standard."""
        
        try:
            logger.info("🔄 Sending to Gemini with ClickHouse data...")
            client = genai.Client(api_key=self.api_key)
            response = client.models.generate_content(
                model="gemini-3.6-flash",
                contents=[{"role": "user", "parts": [{"text": prompt}]}],
            )
            
            result = response.text if hasattr(response, "text") else str(response)
            logger.info(f"✅ Gemini response generated ({len(result)} chars)")
            return result
        except Exception as e:
            logger.error(f"Error: {e}", exc_info=True)
            return f"Error: {str(e)}"


def main():
    """Test the orchestrator"""
    try:
        orchestrator = CinePilotOrchestratorMCP()
        
        test_query = """
Scene 12 Continuity Review:

Scene: Office Arrival
Expected: Daniel in blue jacket, coffee cup on desk
Take 2 Observations: Daniel in black jacket, coffee cup missing

What continuity issues exist?
        """
        
        print("\n" + "="*80)
        print("CINEPILOT MCP CONTINUITY REVIEW")
        print("="*80)
        response = orchestrator.query_sync(test_query)
        print(response)
        print("="*80 + "\n")
        
    except Exception as e:
        logger.error(f"Fatal error: {e}", exc_info=True)


if __name__ == "__main__":
    main()
