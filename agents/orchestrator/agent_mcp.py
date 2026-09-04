"""
CinePilot Orchestrator Agent with ClickHouse MCP Integration
"""
import os
import logging
import asyncio
import uuid
from dotenv import load_dotenv
from google.adk import Agent
from google.adk.runners import InMemoryRunner
from google.genai import types as genai_types
from mcp_clickhouse import run_query

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

        self.adk_agent = Agent(
            name="cinepilot_continuity_agent",
            model="gemini-3.6-flash",
            instruction="""You are a film production continuity supervisor.

            Analyze film scenes and production continuity. Use the provided production
            database context to assess continuity issues. Provide severity levels,
            corrective actions, and reference the approved production standard when
            relevant. Keep the final response concise but actionable."""
        )
        self.adk_runner = InMemoryRunner(agent=self.adk_agent, app_name="cinepilot")
        logger.info("✅ CinePilot Orchestrator with ClickHouse MCP initialized")

    def _run_adk_prompt(self, prompt: str) -> str:
        """Execute the production prompt through Google ADK Agent + InMemoryRunner."""
        collected: list[str] = []
        session_id = f"scene-review-{uuid.uuid4().hex}"

        async def _invoke() -> str:
            await self.adk_runner.session_service.create_session(
                app_name=self.adk_runner.app_name,
                user_id="cinepilot-api",
                session_id=session_id,
            )
            async for event in self.adk_runner.run_async(
                user_id="cinepilot-api",
                session_id=session_id,
                new_message=genai_types.Content(
                    role="user",
                    parts=[genai_types.Part.from_text(text=prompt)],
                ),
            ):
                if getattr(event, "content", None):
                    for part in getattr(event.content, "parts", []) or []:
                        text = getattr(part, "text", None)
                        if text:
                            collected.append(text)
            return "\n".join(collected).strip() or "No response from ADK agent."

        return asyncio.run(_invoke())

    def query_production_decisions(self, scene_id: str) -> str:
        """Query ClickHouse for production decisions via MCP"""
        logger.info(f"🔍 Querying ClickHouse for {scene_id} production decisions...")
        try:
            query = f"""
            SELECT
                decision_id,
                approved_take,
                reason
            FROM cinepilot.production_decisions
            WHERE scene_id = '{scene_id}'
            """

            result = run_query(query)
            logger.info(f"✅ ClickHouse MCP query succeeded")

            # Normalize possible result shapes
            rows = []
            if hasattr(result, "result_rows"):
                rows = result.result_rows
            elif isinstance(result, (list, tuple)):
                rows = list(result)
            elif isinstance(result, dict) and "rows" in result:
                rows = result["rows"]
            else:
                rows = [result]

            try:
                count = len(rows)
            except Exception:
                count = 1

            logger.info(f"   Rows: {count}")

            if rows:
                for row in rows:
                    try:
                        logger.info(f"   Decision: Approved take {row[1]} - {row[2]}")
                    except Exception:
                        logger.info(f"   Decision row: {row}")
                return f"Production decisions: {rows}"
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
        logger.info(f"📊 Production data retrieved: {str(production_data)[:80]}")

        # Build prompt with ClickHouse data
        prompt = f"""You are a film production continuity supervisor.

PRODUCTION DATABASE (via ClickHouse MCP):
{production_data}

USER REQUEST:
{user_request}

Analyze the continuity issues against the production database information above. Provide severity levels, corrective actions, and reference the approved production standard."""

        try:
            logger.info("🔄 Sending to Google ADK Agent + InMemoryRunner with ClickHouse data...")
            result = self._run_adk_prompt(prompt)
            logger.info(f"✅ Gemini response generated ({len(result)} chars)")
            return result
        except Exception as e:
            logger.error(f"ADK runtime error: {e}", exc_info=True)
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