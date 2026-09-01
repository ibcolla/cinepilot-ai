'use client';

export default function DashboardPage() {
  return (
    <div className="p-8">
      <div className="max-w-6xl mx-auto">
        <h1 className="text-4xl font-bold mb-2 text-accent">Dashboard</h1>
        <p className="text-muted-foreground mb-8">Production Intelligence Overview</p>

        {/* Placeholder Content */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          <div className="bg-card border border-border rounded-lg p-6 card-elevated">
            <h3 className="text-lg font-semibold text-foreground mb-2">Scenes Analyzed</h3>
            <p className="text-3xl font-bold text-accent">1</p>
            <p className="text-sm text-muted-foreground mt-2">Scene 12 - Office Arrival</p>
          </div>

          <div className="bg-card border border-border rounded-lg p-6 card-elevated">
            <h3 className="text-lg font-semibold text-foreground mb-2">Issues Detected</h3>
            <p className="text-3xl font-bold text-red-500">2</p>
            <p className="text-sm text-muted-foreground mt-2">Wardrobe + Prop discrepancies</p>
          </div>

          <div className="bg-card border border-border rounded-lg p-6 card-elevated">
            <h3 className="text-lg font-semibold text-foreground mb-2">Agent Status</h3>
            <p className="text-3xl font-bold text-green-500">✓</p>
            <p className="text-sm text-muted-foreground mt-2">Online - MCP Connected</p>
          </div>
        </div>
      </div>
    </div>
  );
}