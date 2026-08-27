"""CinePilot AI Agents Package"""

__version__ = "0.1.0"

try:
    from .orchestrator.agent import CinePilotOrchestrator
    from .script_agent.script_parser import ScriptAgent, SceneData
    from .continuity_agent.vision_analyzer import ContinuityAgent, SceneObservation, ContinuityIssue
    
    __all__ = [
        "CinePilotOrchestrator",
        "ScriptAgent",
        "SceneData",
        "ContinuityAgent",
        "SceneObservation",
        "ContinuityIssue",
    ]
except ImportError as e:
    print(f"Warning: Could not import agents: {e}")