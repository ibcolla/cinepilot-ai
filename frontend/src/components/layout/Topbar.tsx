'use client';

import React, { useState, useEffect } from 'react';
import { AgentStatus } from '../../types';

export function Topbar() {
  const [agentStatus, setAgentStatus] = useState<AgentStatus>({
    online: false,
    lastCheck: new Date().toISOString(),
    mcp_connected: false,
    clickhouse_available: false,
  });

  useEffect(() => {
    const checkStatus = async () => {
      try {
        const response = await fetch('http://localhost:8000/api/agent/status');
        if (response.ok) {
          const data: AgentStatus = await response.json();
          setAgentStatus(data);
        }
      } catch {
        setAgentStatus((prev) => ({
          ...prev,
          lastCheck: new Date().toISOString(),
        }));
      }
    };

    checkStatus();
    const interval = setInterval(checkStatus, 10000);
    return () => clearInterval(interval);
  }, []);

  const getStatusColor = (active: boolean) => active ? 'bg-green-500' : 'bg-red-500';

  return (
    <header className="bg-card border-b border-border px-6 py-4 flex justify-between items-center">
      <h2 className="text-lg font-semibold text-foreground">Continuity Analysis</h2>
      <div className="flex gap-6 text-sm">
        <div className="flex items-center gap-2">
          <div className={`w-2 h-2 rounded-full ${getStatusColor(agentStatus.online)}`}></div>
          <span className="text-muted-foreground">Agent {agentStatus.online ? 'Online' : 'Offline'}</span>
        </div>
        <div className="flex items-center gap-2">
          <div className={`w-2 h-2 rounded-full ${getStatusColor(agentStatus.mcp_connected)}`}></div>
          <span className="text-muted-foreground">MCP {agentStatus.mcp_connected ? 'Connected' : 'Disconnected'}</span>
        </div>
        <div className="flex items-center gap-2">
          <div className={`w-2 h-2 rounded-full ${getStatusColor(agentStatus.clickhouse_available)}`}></div>
          <span className="text-muted-foreground">ClickHouse {agentStatus.clickhouse_available ? 'Ready' : 'Unavailable'}</span>
        </div>
      </div>
    </header>
  );
}
