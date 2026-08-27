"""Scene 12 Acceptance Test"""

import pytest
import sys
sys.path.insert(0, '../agents')

from agents.script_agent.script_parser import ScriptAgent
from agents.continuity_agent.vision_analyzer import ContinuityAgent, SceneObservation


class TestScene12:
    """Test Scene 12: Office Arrival"""
    
    def test_script_analysis(self):
        """Script Agent extracts Scene 12 data"""
        agent = ScriptAgent()
        scene = agent.analyze_scene("Daniel enters office wearing blue jacket with coffee cup")
        
        assert scene.scene_id == "SC12"
        assert "Daniel" in scene.characters
        assert "Blue jacket" in scene.props
        print("✅ Script analysis passed")
    
    def test_take_2_errors(self):
        """Continuity Agent detects errors in Take 2"""
        agent = ContinuityAgent()
        
        observation = SceneObservation(
            take_id="SC12_T002",
            characters=["Daniel"],
            costumes={"Daniel": "Black jacket"},  # WRONG
            props_present=["Laptop", "Phone"],  # MISSING coffee cup
            props_missing=["Coffee cup"]
        )
        
        required = {
            "costumes": {"Daniel": "Blue jacket"},
            "props": ["Coffee cup", "Blue jacket", "Laptop", "Phone"]
        }
        
        issues = agent.analyze_observation(observation, required)
        
        assert len(issues) >= 2
        assert any(i.issue_type == "costume" for i in issues)
        assert any(i.issue_type == "prop" for i in issues)
        print(f"✅ Found {len(issues)} issues in Take 2")


if __name__ == "__main__":
    pytest.main([__file__, "-v", "-s"])