"""
FastAPI Backend for CinePilot AI
Wraps the existing CinePilotOrchestratorMCP agent and exposes REST endpoints
"""
import os
import re
import logging
from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from starlette.concurrency import run_in_threadpool
from agents.orchestrator.agent_mcp import CinePilotOrchestratorMCP

# Logging
logging.basicConfig(level=os.getenv("LOG_LEVEL", "INFO"))
logger = logging.getLogger(__name__)

# ============================================================================
# Pydantic Models (matching frontend/src/types/index.ts)
# ============================================================================

class ContinuityIssue(BaseModel):
    id: str
    category: str
    severity: str  # 'CRITICAL' | 'HIGH' | 'MEDIUM' | 'LOW'
    confidence: float  # 0.0 to 1.0
    expected: str
    observed: str
    impact: str
    recommendation: str

class SceneAnalysis(BaseModel):
    sceneId: str
    takeId: str
    status: str  # 'ANALYSIS_COMPLETE' | 'PENDING' | 'ERROR'
    issues: List[ContinuityIssue]
    approvedStandard: str
    analysisTimestamp: Optional[str] = None
    agentConfidence: Optional[float] = None

class AnalysisRequest(BaseModel):
    sceneId: str
    takeId: str
    observations: str
    imageUrl: Optional[str] = None

class AnalysisResponse(BaseModel):
    success: bool
    analysis: Optional[SceneAnalysis] = None
    error: Optional[str] = None
    processingTime: int  # milliseconds

class AgentStatus(BaseModel):
    online: bool
    lastCheck: str
    mcp_connected: bool
    clickhouse_available: bool

# ============================================================================
# Markdown Parser
# ============================================================================

def extract_field(text: str, key_pattern: str, default: str = "Unknown") -> str:
    """Extract a field value after a pattern"""
    match = re.search(
        rf"(?:{key_pattern})[\s:\*]*([^\n]+)",
        text,
        re.IGNORECASE
    )
    if match and match.group(1) is not None:
        value = match.group(1).strip()
        value = re.sub(r"[\*`]", "", value).strip()
        value = re.sub(r"\s+", " ", value)
        if value:
            return value
    return default

def parse_markdown_to_issues(markdown_text: str, scene_id: str, take_id: str) -> tuple[List[ContinuityIssue], str]:
    """
    Parse Gemini's Markdown continuity report into structured ContinuityIssue objects.
    """
    issues: List[ContinuityIssue] = []
    approved_standard = ""
    
    logger.info(f"Parsing markdown ({len(markdown_text)} chars) for {scene_id}/{take_id}")
    
    # Extract approved standard if mentioned
    approved_match = re.search(
        r"(?:Approved Production Standard Reference|Approved Standard|Approved Take|Approved Decision)[\s:\*]+([^\n]+)",
        markdown_text,
        re.IGNORECASE
    )
    if approved_match and approved_match.group(1):
        approved_standard = re.sub(r"[\*`]", "", approved_match.group(1)).strip()
        logger.info(f"Approved standard: {approved_standard}")
    
    # Split by potential issue delimiters
    issue_blocks = re.split(
        r"(?:^|\n)(?:#{1,4}\s*|\*\*)*\s*(?:Issue\s*\d+|Issue|\d+\.)",
        markdown_text,
        flags=re.IGNORECASE
    )
    
    issue_id = 1
    for block in issue_blocks:
        if not block.strip() or len(block.strip()) < 30 or "CONTINUITY SUPERVISOR" in block:
            continue
        
        # Extract severity
        severity = "MEDIUM"
        severity_match = re.search(
            r"(?:Severity|severity)[\s:\*]*([A-Z]+)",
            block,
            re.IGNORECASE
        )
        if severity_match:
            sev = severity_match.group(1).upper()
            if sev in ["CRITICAL", "HIGH", "MEDIUM", "LOW"]:
                severity = sev
        
        # Extract category
        category = extract_field(block, "Category", "General")
        if category == "General":
            if re.search(r"(?:Wardrobe|jacket|shirt|pants|clothing)", block, re.IGNORECASE):
                category = "Wardrobe"
            elif re.search(r"(?:Prop|props|cup|coffee|object)", block, re.IGNORECASE):
                category = "Prop"
            elif re.search(r"(?:Lighting|light|brightness)", block, re.IGNORECASE):
                category = "Lighting"
            elif re.search(r"(?:Location|set|background|environment)", block, re.IGNORECASE):
                category = "Location"
        
        # Extract confidence
        confidence = 0.85
        conf_match = re.search(
            r"(?:Confidence|confidence)[\s:\*]*([0-9.]+)\s*%?",
            block,
            re.IGNORECASE
        )
        if conf_match:
            try:
                conf_val = float(conf_match.group(1))
                if conf_val > 1:
                    confidence = conf_val / 100.0
                else:
                    confidence = conf_val
                confidence = min(1.0, max(0.0, confidence))
            except ValueError:
                pass
        
        # Extract fields
        expected = extract_field(block, "Expected|What was expected|Standard", "Unknown")
        observed = extract_field(block, "Observed|What was observed|Actual", "Unknown")
        impact = extract_field(block, "Impact|Impact on continuity|Effect", "Unknown")
        recommendation = extract_field(block, "Recommendation|Recommended corrective action|Action|Solution", "Unknown")
        
        if expected != "Unknown" or observed != "Unknown" or category != "General":
            issue = ContinuityIssue(
                id=f"issue_{issue_id:03d}",
                category=category,
                severity=severity,
                confidence=confidence,
                expected=expected,
                observed=observed,
                impact=impact if impact != "Unknown" else f"{category} discrepancy detected",
                recommendation=recommendation if recommendation != "Unknown" else f"Review {category.lower()} for corrections"
            )
            issues.append(issue)
            issue_id += 1
            logger.info(f"Parsed issue: {issue.category} ({issue.severity})")
    
    if not issues and len(markdown_text) > 100:
        logger.warning("No structured issues found, creating generic issue from full text")
        issues.append(
            ContinuityIssue(
                id="issue_001",
                category="General",
                severity="HIGH",
                confidence=0.75,
                expected="Approved take",
                observed="Current take",
                impact=markdown_text[:200],
                recommendation="Review agent output for details"
            )
        )
    
    if not approved_standard:
        approved_standard = "Production standard from ClickHouse"
    
    return issues, approved_standard

# ============================================================================
# FastAPI Application
# ============================================================================

app = FastAPI(
    title="CinePilot AI Backend",
    description="Film production continuity analysis with Gemini + ClickHouse",
    version="0.1.0"
)

# CORS middleware for frontend integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://localhost:3001",
        "http://127.0.0.1:3000",
        "http://127.0.0.1:3001",
        "https://cinepilot-frontend-3fhj5qvq4q-uc.a.run.app"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize orchestrator
try:
    orchestrator = CinePilotOrchestratorMCP()
    AGENT_INITIALIZED = True
    logger.info("✅ CinePilotOrchestratorMCP initialized")
except Exception as e:
    AGENT_INITIALIZED = False
    logger.warning(f"⚠️  Agent initialization failed (expected if env vars not set): {e}")

# ============================================================================
# Endpoints
# ============================================================================

@app.get("/health", tags=["Health"])
async def health_check():
    """Health check endpoint"""
    return {
        "status": "ok",
        "agent_initialized": AGENT_INITIALIZED,
        "timestamp": datetime.utcnow().isoformat()
    }

@app.get("/api/agent/status", response_model=AgentStatus, tags=["Agent"])
async def agent_status():
    """Get agent status"""
    return AgentStatus(
        online=AGENT_INITIALIZED,
        lastCheck=datetime.utcnow().isoformat(),
        mcp_connected=AGENT_INITIALIZED,
        clickhouse_available=AGENT_INITIALIZED
    )

@app.post("/api/analyze-scene", response_model=AnalysisResponse, tags=["Analysis"])
async def analyze_scene(request: AnalysisRequest):
    """
    Analyze a scene for continuity issues.
    """
    start_time = datetime.utcnow()
    
    try:
        if not AGENT_INITIALIZED:
            raise HTTPException(
                status_code=503,
                detail="Agent not initialized. Check GEMINI_API_KEY and other env vars."
            )
        
        logger.info(f"📽️  Analyzing {request.sceneId}/{request.takeId}")
        logger.info(f"   Observations: {request.observations[:100]}...")
        
        # Build prompt for agent
        agent_prompt = f"""
Scene {request.sceneId} - Take {request.takeId}
Continuity Review:

Current Observations:
{request.observations}

Analyze the continuity issues. Provide:
1. For each issue found:
   - Severity (CRITICAL, HIGH, MEDIUM, LOW)
   - Category (Wardrobe, Prop, Lighting, Location, etc.)
   - Confidence (0.0 to 1.0)
   - What was expected (from production standard)
   - What was observed
   - Impact on continuity
   - Recommended corrective action
"""
        
        # Call the agent in threadpool to avoid blocking event loop
        markdown_response = await run_in_threadpool(orchestrator.query_sync, agent_prompt)
        logger.info(f"✅ Agent returned {len(markdown_response)} chars")
        
        # Parse markdown to structured issues
        issues, approved_standard = parse_markdown_to_issues(
            markdown_response,
            request.sceneId,
            request.takeId
        )
        
        # Build response
        analysis = SceneAnalysis(
            sceneId=request.sceneId,
            takeId=request.takeId,
            status="ANALYSIS_COMPLETE",
            issues=issues,
            approvedStandard=approved_standard,
            analysisTimestamp=datetime.utcnow().isoformat(),
            agentConfidence=sum(i.confidence for i in issues) / len(issues) if issues else 0.0
        )
        
        elapsed_ms = int((datetime.utcnow() - start_time).total_seconds() * 1000)
        
        return AnalysisResponse(
            success=True,
            analysis=analysis,
            processingTime=elapsed_ms
        )
    
    except Exception as e:
        elapsed_ms = int((datetime.utcnow() - start_time).total_seconds() * 1000)
        logger.error(f"❌ Analysis failed: {e}", exc_info=True)
        return AnalysisResponse(
            success=False,
            error=str(e),
            processingTime=elapsed_ms
        )

@app.get("/api/dashboard", tags=["Dashboard"])
async def dashboard():
    """Get dashboard metrics"""
    return {
        "scenes_analyzed": 1,
        "issues_detected": 2,
        "agent_online": AGENT_INITIALIZED
    }

# ============================================================================
# Main
# ============================================================================

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        log_level="info"
    )