'use client';

import type { SceneAnalysis } from '../../types';

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

export default function ContinuityPage() {
  return (
    <div className="p-8">
      <div className="max-w-5xl mx-auto">
        <div className="mb-8">
          <h1 className="text-4xl font-bold mb-2 text-accent">Continuity</h1>
          <p className="text-muted-foreground">Scene 12 continuity review and approved standard</p>
        </div>

        <div className="bg-card border border-border rounded-lg p-6 mb-8 card-elevated">
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
            <div>
              <p className="text-sm text-muted-foreground">Scene</p>
              <p className="text-xl font-bold text-foreground">{fixtureAnalysis.sceneId}</p>
            </div>
            <div>
              <p className="text-sm text-muted-foreground">Take</p>
              <p className="text-xl font-bold text-foreground">{fixtureAnalysis.takeId}</p>
            </div>
            <div>
              <p className="text-sm text-muted-foreground">Status</p>
              <p className="text-xl font-bold text-green-500">{fixtureAnalysis.status}</p>
            </div>
            <div>
              <p className="text-sm text-muted-foreground">Approved Standard</p>
              <p className="text-xl font-bold text-accent">{fixtureAnalysis.approvedStandard}</p>
            </div>
          </div>
        </div>

        <div className="space-y-4">
          <h2 className="text-2xl font-bold text-foreground mb-4">
            Detected Issues ({fixtureAnalysis.issues.length})
          </h2>

          {fixtureAnalysis.issues.map((issue) => (
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
                  <p className="ml-4 text-foreground font-medium text-accent">{issue.recommendation}</p>
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
