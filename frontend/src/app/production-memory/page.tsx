const productionMemory = {
  sceneId: 'SC12',
  approvedTake: 'SC12_T001',
  approvedReason:
    'Approved master with correct wardrobe continuity, desk prop present, and no continuity mismatch across the take.',
  decisionDate: '2026-08-31',
};

export default function ProductionMemoryPage() {
  return (
    <div className="p-8">
      <div className="max-w-4xl mx-auto">
        <div className="mb-8">
          <h1 className="text-4xl font-bold mb-2 text-accent">Production Memory</h1>
          <p className="text-muted-foreground">Approved decisions and continuity history</p>
        </div>

        <div className="bg-card border border-border rounded-lg p-6 mb-6 card-elevated">
          <div className="grid gap-6 md:grid-cols-3">
            <div>
              <p className="text-sm text-muted-foreground">Scene</p>
              <p className="text-xl font-bold text-foreground">{productionMemory.sceneId}</p>
            </div>
            <div>
              <p className="text-sm text-muted-foreground">Approved Take</p>
              <p className="text-xl font-bold text-accent">{productionMemory.approvedTake}</p>
            </div>
            <div>
              <p className="text-sm text-muted-foreground">Decision Date</p>
              <p className="text-xl font-bold text-foreground">{productionMemory.decisionDate}</p>
            </div>
          </div>
        </div>

        <div className="bg-card border border-border rounded-lg p-6 card-elevated">
          <h2 className="text-2xl font-bold text-foreground mb-4">Approved Standard</h2>
          <p className="text-foreground leading-relaxed">{productionMemory.approvedReason}</p>
        </div>
      </div>
    </div>
  );
}
