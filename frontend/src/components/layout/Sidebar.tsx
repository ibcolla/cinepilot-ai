'use client';

import { usePathname } from 'next/navigation';
import Link from 'next/link';

export function Sidebar() {
  const pathname = usePathname();

  const links = [
    { href: '/', label: 'Dashboard', icon: '🎬' },
    { href: '/scenes/scene-12', label: 'Scene 12', icon: '📹' },
    { href: '/continuity', label: 'Continuity', icon: '✓' },
    { href: '/production-memory', label: 'Production Memory', icon: '💾' },
  ];

  return (
    <aside className="w-64 bg-card border-r border-border p-6">
      <h1 className="text-2xl font-bold text-accent mb-8">CinePilot</h1>
      <nav className="space-y-2">
        {links.map((link) => (
          <Link
            key={link.href}
            href={link.href}
            className={`block px-4 py-2 rounded-lg transition-colors ${
              pathname === link.href
                ? 'bg-accent text-accent-foreground'
                : 'text-muted-foreground hover:bg-card-elevated'
            }`}
          >
            {link.icon} {link.label}
          </Link>
        ))}
      </nav>
    </aside>
  );
}
