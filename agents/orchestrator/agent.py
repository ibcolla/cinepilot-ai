"""CinePilot Orchestrator Agent with Gemini"""

import os
import logging
from dotenv import load_dotenv
from google import genai

load_dotenv()
logging.basicConfig(level=os.getenv("AGENT_LOG_LEVEL", "INFO"))
logger = logging.getLogger(__name__)


class CinePilotOrchestrator:
    """Main orchestrator agent using Gemini"""
    
    def __init__(self):
        """Initialize with Gemini API"""
        self.api_key = os.getenv("GEMINI_API_KEY")
        if not self.api_key:
            raise ValueError("GEMINI_API_KEY not set in .env")
        
        self.client = genai.Client(api_key=self.api_key)
        logger.info("✅ CinePilot Orchestrator initialized with Gemini")
    
    def query(self, user_request: str) -> str:
        """Process a continuity review request"""
        logger.info(f"Processing: {user_request}")
        
        system_prompt = """You are CinePilot AI, a film production continuity supervisor.
        
Your role:
- Analyze film scenes and production continuity
- Detect costume, prop, and environmental inconsistencies
- Provide actionable recommendations to filmmakers

Be precise, cite confidence levels, and recommend specific corrective actions."""
        
        try:
            response = self.client.models.generate_content(
                model="gemini-3.6-flash",
                contents=[
                    {
                        "role": "user",
                        "parts": [
                            {
                                "text": f"{system_prompt}\n\n{user_request}"
                            }
                        ]
                    }
                ]
            )
            
            result = response.text if hasattr(response, 'text') else str(response)
            logger.info(f"Response: {result[:100]}...")
            return result
        except Exception as e:
            logger.error(f"Error: {e}")
            return f"Error: {str(e)}"


def main():
    """Test the orchestrator"""
    orchestrator = CinePilotOrchestrator()
    
    test_query = """
    Scene 12: Office Arrival
    
    Expected:
    - Daniel wears a blue jacket
    - Coffee cup on desk
    
    Take 2 observation:
    - Daniel wearing black jacket
    - No coffee cup visible
    
    What continuity issues should we flag?
    """
    
    print("\n" + "="*80)
    print("CINEPILOT CONTINUITY REVIEW")
    print("="*80)
    response = orchestrator.query(test_query)
    print(response)
    print("="*80 + "\n")


if __name__ == "__main__":
    main()