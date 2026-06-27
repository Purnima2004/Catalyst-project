import React from 'react'
import { Link, useLocation } from 'react-router-dom'

const steps = [
  { label: 'Home', path: '/' },
  { label: 'Setup', path: '/setup' },
  { label: 'Interview', path: '/assessment' },
  { label: 'Results', path: '/results' },
]

export default function Navbar() {
  const { pathname } = useLocation()

  return (
    <header className="fixed top-0 inset-x-0 z-50 border-b border-border bg-surface/90 backdrop-blur-sm">
      <div className="max-w-5xl mx-auto px-5 h-14 flex items-center justify-between">
        <Link to="/" className="text-[15px] font-semibold text-ink tracking-tight">
          Impetus
        </Link>

        <nav className="flex items-center gap-1">
          {steps.map((step) => {
            const active = pathname === step.path
            return (
              <Link
                key={step.path}
                to={step.path}
                className={`px-3 py-1.5 rounded-md text-[13px] transition-colors
                  ${active
                    ? 'bg-stone-100 text-ink font-medium'
                    : 'text-ink-muted hover:text-ink hover:bg-stone-50'}`}
              >
                {step.label}
              </Link>
            )
          })}
        </nav>
      </div>
    </header>
  )
}
