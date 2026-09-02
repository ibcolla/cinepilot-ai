'use client';

import { SceneAnalysis } from '../../../types';
import { analyzeScene } from '../../../services/api';
import { useState, useEffect } from 'react';

// Fixture data for Scene 12 (fallback/initial state)
const fixtureAnalysis: SceneAnalysis = {
  sceneId: 'SC12',
  takeId: 'SC12_T002',
  status: 'ANALYSIS_COMPLETE',
  approvedStandard: 'SC12_DECISION_001 (Take 1 - Approved Master)',
  issues: [
    {
      id: 'issue_001',
      category: 'Wardrobe',
      severity: 'CRITICAL',
      confidence: 0.96,
      expected: 'Daniel in blue jacket',
      observed: 'Daniel in black jacket',
      impact: 'Critical continuity break - jacket color change between takes',
      recommendation: 'Do not use Take 2. Use approved Take 1 (SC12_T001).',
    },
    {
      id: 'issue_002',
      category: 'Prop',
      severity: 'HIGH',
      confidence: 0.91,
      expected: 'Coffee cup on desk',
      observed: 'Coffee cup missing',
      impact: 'Set dressing discrepancy - missing required prop',
      recommendation: 'Add coffee cup to desk or re-shoot Take 2 with corrected props.',
    },
  ],
};

export default function Scene12Page() {
  const [analysis, setAnalysis] = useState<SceneAnalysis>(fixtureAnalysis);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [backendAvailable, setBackendAvailable] = useState(false);
  const [lastUpdated, setLastUpdated] = useState<string | null>(null);

  // Check if backend is available on mount
  useEffect(() => {
    const checkBackend = async () => {
      try {
        const response = await fetch('http://localhost:8000/health', {
          signal: AbortSignal.timeout(3000),
        });
        setBackendAvailable(response.ok);
      } catch {
        setBackendAvailable(false);
      }
    };

    checkBackend();
  }, []);

  const handleAnalyzeCurrentTake = async () => {
    setIsLoading(true);
    setError(null);

    try {
      const response = await analyzeScene({
        sceneId: 'SC12',
        takeId: 'SC12_T002',
        observations: `
Scene 12 - Office Arrival
Current Take Observations:
- Daniel's wardrobe: black jacket
- Props: coffee cup missing from desk
- Set dressing: minimal
- Lighting: office fluorescent

Compare against approved production standard for continuity issues.
        `.trim(),
      });

      if (response.success && response.analysis) {
        setAnalysis(response.analysis);
        setLastUpdated(new Date().toLocaleString());
      } else {
        setError(response.error || 'Analysis failed');
      }
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Unknown error');
    } finally {
      setIsLoading(false);
    }
  };

  const getSeverityColor = (severity: string) => {
    switch (severity) {
      case 'CRITICAL':
        return 'text-red-500 bg-red-500/10 border-red-500/30';
      case 'HIGH':
        return 'text-orange-500 bg-orange-500/10 border-orange-500/30';
      case 'MEDIUM':
        return 'text-yellow-500 bg-yellow-500/10 border-yellow-500/30';
      case 'LOW':
        return 'text-green-500 bg-green-500/10 border-green-500/30';
      default:
        return 'text-muted-foreground';
    }
  };

  return (
    <div className="p-8">
      <div className="max-w-4xl mx-auto">
        {/* Header */}
        <div className="mb-8">
          <h1 className="text-4xl font-bold mb-2 text-accent">Scene 12 - Office Arrival</h1>
          <p className="text-muted-foreground">
            Continuity Analysis: {analysis.approvedStandard}
          </p>
        </div>

        {/* Status Card */}
        <div className="bg-card border border-border rounded-lg p-6 mb-8 card-elevated">
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
            <div>
              <p className="text-sm text-muted-foreground">Scene</p>
              <p className="text-xl font-bold text-foreground">{analysis.sceneId}</p>
            </div>
            <div>
              <p className="text-sm text-muted-foreground">Take</p>
              <p className="text-xl font-bold text-foreground">{analysis.takeId}</p>
            </div>
            <div>
              <p className="text-sm text-muted-foreground">Status</p>
              <p className="text-xl font-bold text-green-500">{analysis.status}</p>
            </div>
            <div>
              <p className="text-sm text-muted-foreground">Issues</p>
              <p className="text-xl font-bold text-accent">{analysis.issues.length}</p>
            </div>
          </div>
        </div>

        {/* Backend Status */}
        {!backendAvailable && (
          <div className="bg-yellow-500/10 border border-yellow-500/30 rounded-lg p-4 mb-6 text-yellow-500">
            ⚠️ Backend not available. Showing fixture data. To enable live analysis, start the FastAPI server:
            <code className="block mt-2 bg-black/20 p-2 rounded text-sm font-mono">
              python3 -m uvicorn api:app --reload
            </code>
          </div>
        )}

        {/* Error Message */}
        {error && (
          <div className="bg-red-500/10 border border-red-500/30 rounded-lg p-4 mb-6 text-red-500">
            ❌ Error: {error}
          </div>
        )}

        {/* Analyze Button */}
        <div className="mb-8">
          <button
            onClick={handleAnalyzeCurrentTake}
            disabled={isLoading || !backendAvailable}
            className={`
              px-6 py-3 rounded-lg font-semibold transition-all duration-200
              ${
                isLoading
                  ? 'bg-accent/50 text-accent-foreground/50 cursor-not-allowed'
                  : backendAvailable
                    ? 'bg-accent text-accent-foreground hover:bg-accent/90 cursor-pointer'
                    : 'bg-muted text-muted-foreground cursor-not-allowed'
              }
            `}
          >
            {isLoading
              ? '🔄 Analyzing... (Gemini is reasoning)'
              : backendAvailable
                ? '📹 Analyze Current Take'
                : '⚠️ Analyze Current Take (backend offline)'}
          </button>
          {lastUpdated && (
            <p className="text-sm text-muted-foreground mt-3">Last live analysis: {lastUpdated}</p>
          )}
        </div>

        {/* Issues List */}
        <div className="space-y-4">
          <h2 className="text-2xl font-bold text-foreground mb-4">
            Detected Issues {analysis.issues.length > 0 && `(${analysis.issues.length})`}
          </h2>

          {analysis.issues.length === 0 ? (
            <div className="bg-card border border-border rounded-lg p-8 text-center text-muted-foreground">
              No continuity issues detected.
            </div>
          ) : (
            analysis.issues.map((issue) => (
              <div
                key={issue.id}
                className={`bg-card border rounded-lg p-6 card-elevated ${getSeverityColor(issue.severity)}`}
              >
                <div className="flex items-start justify-between mb-4">
                  <div>
                    <h3 className="text-lg font-semibold text-foreground">{issue.category}</h3>
                    <span
                      className={`inline-block mt-2 px-3 py-1 rounded-full text-sm font-medium border ${getSeverityColor(
                        issue.severity
                      )}`}
                    >
                      {issue.severity} ({Math.round(issue.confidence * 100)}%)
                    </span>
                  </div>
                </div>

                <div className="space-y-3 text-foreground text-sm">
                  <div>
                    <p className="text-muted-foreground font-semibold">Expected:</p>
                    <p className="ml-4 text-foreground">{issue.expected}</p>
                  </div>
                  <div>
                    <p className="text-muted-foreground font-semibold">Observed:</p>
                    <p className="ml-4 text-foreground">{issue.observed}</p>
                  </div>
                  <div>
                    <p className="text-muted-foreground font-semibold">Impact:</p>
                    <p className="ml-4 text-foreground">{issue.impact}</p>
                  </div>
                  <div>
                    <p className="text-muted-foreground font-semibold">Recommendation:</p>
                    <p className="ml-4 text-foreground font-medium text-accent">
                      {issue.recommendation}
                    </p>
                  </div>
                </div>
              </div>
            ))
          )}
        </div>
      </div>
    </div>
  );
}
