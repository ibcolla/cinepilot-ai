/**
 * CinePilot AI - Frontend Data Contract
 * Defines the structure of data exchanged between backend and UI
 */

export type SeverityLevel = 'CRITICAL' | 'HIGH' | 'MEDIUM' | 'LOW';
export type AnalysisStatus = 'ANALYSIS_COMPLETE' | 'PENDING' | 'ERROR';

export interface ContinuityIssue {
  id: string;
  category: string; // e.g., "Wardrobe", "Prop", "Lighting", "Location"
  severity: SeverityLevel;
  confidence: number; // 0.0 to 1.0
  expected: string; // What the approved standard specifies
  observed: string; // What was actually observed
  impact: string; // Description of impact on continuity
  recommendation: string; // Specific corrective action
}

export interface SceneAnalysis {
  sceneId: string;
  takeId: string;
  status: AnalysisStatus;
  issues: ContinuityIssue[];
  approvedStandard: string; // Reference to the approved production decision
  analysisTimestamp?: string; // ISO 8601 timestamp
  agentConfidence?: number; // Overall confidence in the analysis
}

export interface Scene {
  id: string;
  title: string;
  location: string;
  characters: string[];
  props: string[];
  createdAt: string;
}

export interface Take {
  id: string;
  sceneId: string;
  takeNumber: number;
  status: 'APPROVED' | 'REJECTED' | 'PENDING';
  notes?: string;
}

export interface ProductionMemory {
  sceneId: string;
  approvedTake: string;
  approvedReason: string;
  decisionDate: string;
}

export interface AgentStatus {
  online: boolean;
  lastCheck: string; // ISO 8601 timestamp
  mcp_connected: boolean;
  clickhouse_available: boolean;
}

export interface AnalysisRequest {
  sceneId: string;
  takeId: string;
  observations: string; // User input describing what they see
  imageUrl?: string; // Optional image of the take
}

export interface AnalysisResponse {
  success: boolean;
  analysis?: SceneAnalysis;
  error?: string;
  processingTime: number; // milliseconds
}