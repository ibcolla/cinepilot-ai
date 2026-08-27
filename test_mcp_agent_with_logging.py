import os
import logging
from dotenv import load_dotenv
from agents.orchestrator.agent_mcp import CinePilotOrchestratorMCP

load_dotenv()

# Enable detailed logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

orchestrator = CinePilotOrchestratorMCP()

query = """
Scene 12: Check against production decisions.
What continuity issues exist in Take 2?
"""

print("\n" + "="*80)
print("AGENT REQUEST")
print("="*80)
print(query)
print("="*80 + "\n")

response = orchestrator.query_sync(query)

print("\n" + "="*80)
print("AGENT RESPONSE")
print("="*80)
print(response)
print("="*80 + "\n")
