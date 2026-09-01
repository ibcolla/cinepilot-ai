/**
 * CinePilot API Client
 * Communicates with backend FastAPI server for scene analysis
 */

import {
  AnalysisRequest,
  AnalysisResponse,
  AgentStatus,
} from '../types';

const API_BASE_URL = process.env.NEXT_PUBLIC_API_BASE_URL || 'http://localhost:8000';
const API_TIMEOUT_MS = 45000; // 45 seconds for Gemini reasoning

/**
 * Analyze a scene for continuity issues
 */
export async function analyzeScene(
  request: AnalysisRequest
): Promise<AnalysisResponse> {
  try {
    const controller = new AbortController();
    const timeoutId = setTimeout(() => controller.abort(), API_TIMEOUT_MS);

    const response = await fetch(`${API_BASE_URL}/api/analyze-scene`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(request),
      signal: controller.signal,
    });

    clearTimeout(timeoutId);

    if (!response.ok) {
      throw new Error(`HTTP ${response.status}: ${response.statusText}`);
    }

    const data: AnalysisResponse = await response.json();
    return data;
  } catch (error) {
    if (error instanceof Error && error.name === 'AbortError') {
      return {
        success: false,
        error: 'Request timeout. Analysis took longer than 45 seconds.',
        processingTime: API_TIMEOUT_MS,
      };
    }

    const errorMessage = error instanceof Error ? error.message : 'Unknown error';
    return {
      success: false,
      error: `Failed to analyze scene: ${errorMessage}`,
      processingTime: 0,
    };
  }
}

/**
 * Get agent status (online, MCP connected, ClickHouse available)
 */
export async function getAgentStatus(): Promise<AgentStatus | null> {
  try {
    const controller = new AbortController();
    const timeoutId = setTimeout(() => controller.abort(), 5000);

    const response = await fetch(`${API_BASE_URL}/api/agent/status`, {
      signal: controller.signal,
    });

    clearTimeout(timeoutId);

    if (!response.ok) {
      return null;
    }

    const data: AgentStatus = await response.json();
    return data;
  } catch {
    return null;
  }
}

/**
 * Get dashboard metrics
 */
export async function getDashboardMetrics(): Promise<{
  scenes_analyzed: number;
  issues_detected: number;
  agent_online: boolean;
} | null> {
  try {
    const controller = new AbortController();
    const timeoutId = setTimeout(() => controller.abort(), 5000);

    const response = await fetch(`${API_BASE_URL}/api/dashboard`, {
      signal: controller.signal,
    });

    clearTimeout(timeoutId);

    if (!response.ok) {
      return null;
    }

    const data = await response.json();
    return data;
  } catch {
    return null;
  }
}

/**
 * Check if backend is available
 */
export async function isBackendAvailable(): Promise<boolean> {
  try {
    const controller = new AbortController();
    const timeoutId = setTimeout(() => controller.abort(), 3000);

    const response = await fetch(`${API_BASE_URL}/health`, {
      signal: controller.signal,
    });

    clearTimeout(timeoutId);
    return response.ok;
  } catch {
    return false;
  }
}
