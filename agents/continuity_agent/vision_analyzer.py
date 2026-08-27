"""Continuity Vision Agent - Analyzes scene observations"""

import logging
from dataclasses import dataclass

logger = logging.getLogger(__name__)


@dataclass
class SceneObservation:
    """Observation from a filmed take"""
    take_id: str
    characters: list[str]
    costumes: dict[str, str]
    props_present: list[str]
    props_missing: list[str]


@dataclass
class ContinuityIssue:
    """Detected continuity discrepancy"""
    issue_type: str
    severity: str
    description: str
    confidence: float


class ContinuityAgent:
    """Detect continuity issues in filmed takes"""
    
    def __init__(self):
        logger.info("Initializing Continuity Agent")
    
    def analyze_observation(
        self,
        observation: SceneObservation,
        required_continuity: dict
    ) -> list[ContinuityIssue]:
        """Analyze observations and detect continuity issues"""
        logger.info(f"Analyzing {observation.take_id}")
        
        issues = []
        
        # Check costumes
        for character, expected_costume in required_continuity.get("costumes", {}).items():
            if character in observation.costumes:
                actual = observation.costumes[character]
                if actual.lower() != expected_costume.lower():
                    issues.append(ContinuityIssue(
                        issue_type="costume",
                        severity="critical",
                        description=f"{character}: {actual} vs {expected_costume}",
                        confidence=0.96
                    ))
        
        # Check props
        for required_prop in required_continuity.get("props", []):
            if required_prop not in observation.props_present:
                issues.append(ContinuityIssue(
                    issue_type="prop",
                    severity="high",
                    description=f"Missing: {required_prop}",
                    confidence=0.91
                ))
        
        logger.info(f"Found {len(issues)} issues in {observation.take_id}")
        return issues