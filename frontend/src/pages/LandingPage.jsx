import React from 'react'
import { useNavigate } from 'react-router-dom'
import { ArrowRight, FileText, MessageSquare, ListChecks } from 'lucide-react'
import Navbar from '../components/Navbar.jsx'

const steps = [
  {
    icon: FileText,
    title: 'Upload resume + job post',
    desc: 'We compare what the role asks for against what your resume actually shows.',
  },
  {
    icon: MessageSquare,
    title: 'Short technical interview',
    desc: 'A few scenario-based questions — the kind you’d get in a real screen, not trivia.',
  },
  {
    icon: ListChecks,
    title: 'Scores and a study plan',
    desc: 'You get honest feedback per skill, plus links to resources worth your time.',
  },
]

export default function LandingPage() {
  const navigate = useNavigate()

  return (
    <div className="min-h-screen">
      <Navbar />

      <main className="max-w-5xl mx-auto px-5 pt-28 pb-20">
        <section className="grid lg:grid-cols-2 gap-12 lg:gap-16 items-center py-8 lg:py-16">
          <div>
            <p className="text-sm text-ink-muted mb-4">For developers prepping for a specific role</p>
            <h1 className="font-serif text-4xl sm:text-[2.75rem] leading-[1.15] text-ink mb-5">
              Find the gap between your resume and the job.
            </h1>
            <p className="text-[15px] text-ink-muted leading-relaxed mb-8 max-w-md">
              Impetus reads your resume next to a job description, runs a quick technical
              interview on the skills that matter, and tells you what to work on next.
            </p>
            <div className="flex flex-wrap gap-3">
              <button
                onClick={() => navigate('/setup')}
                className="inline-flex items-center gap-2 px-5 py-2.5 rounded-lg bg-ink text-white text-sm font-medium hover:bg-stone-800 transition-colors"
              >
                Start free
                <ArrowRight size={16} />
              </button>
              <a
                href="https://github.com/Purnima2004/Impetus-project"
                target="_blank"
                rel="noreferrer"
                className="inline-flex items-center px-5 py-2.5 rounded-lg border border-border-strong text-sm font-medium text-ink-muted hover:text-ink hover:border-stone-400 transition-colors"
              >
                View on GitHub
              </a>
            </div>
          </div>

          {/* Realistic preview — no fake names or sci-fi IDs */}
          <div className="rounded-xl border border-border bg-surface shadow-card p-5 sm:p-6">
            <div className="flex items-center justify-between mb-5 pb-4 border-b border-border">
              <div>
                <p className="text-xs text-ink-faint mb-0.5">Target role</p>
                <p className="text-sm font-medium text-ink">Backend Engineer</p>
              </div>
              <span className="text-xs text-ink-muted bg-stone-100 px-2 py-1 rounded">3 skills to check</span>
            </div>

            <div className="space-y-4 mb-5">
              {[
                { skill: 'Django', score: 3.2, note: 'Knows basics, weak on production patterns' },
                { skill: 'PostgreSQL', score: 2.1, note: 'Mentioned MySQL only — indexing gaps' },
                { skill: 'Docker', score: 1.8, note: 'Not on resume — needs hands-on practice' },
              ].map((row) => (
                <div key={row.skill}>
                  <div className="flex justify-between text-sm mb-1.5">
                    <span className="font-medium text-ink">{row.skill}</span>
                    <span className="text-ink-muted">{row.score} / 5</span>
                  </div>
                  <div className="h-1.5 rounded-full bg-stone-100 overflow-hidden mb-1">
                    <div
                      className="h-full rounded-full bg-accent"
                      style={{ width: `${(row.score / 5) * 100}%` }}
                    />
                  </div>
                  <p className="text-xs text-ink-faint">{row.note}</p>
                </div>
              ))}
            </div>

            <div className="rounded-lg bg-stone-50 border border-border p-3.5">
              <p className="text-xs font-medium text-ink-muted mb-1">Sample interview question</p>
              <p className="text-sm text-ink leading-relaxed">
                “You need to add auth to a Django REST API. Walk me through how you’d structure
                that — models, permissions, and token handling.”
              </p>
            </div>
          </div>
        </section>

        <section className="py-16 border-t border-border">
          <h2 className="text-lg font-semibold text-ink mb-2">How it works</h2>
          <p className="text-sm text-ink-muted mb-10 max-w-lg">
            Three steps. Takes about 15–20 minutes if you answer properly.
          </p>

          <div className="grid sm:grid-cols-3 gap-6">
            {steps.map(({ icon: Icon, title, desc }, i) => (
              <div key={title} className="rounded-xl border border-border bg-surface p-5 shadow-card">
                <div className="w-9 h-9 rounded-lg bg-accent-soft text-accent flex items-center justify-center mb-4">
                  <Icon size={18} />
                </div>
                <p className="text-xs text-ink-faint mb-1">Step {i + 1}</p>
                <h3 className="text-[15px] font-semibold text-ink mb-2">{title}</h3>
                <p className="text-sm text-ink-muted leading-relaxed">{desc}</p>
              </div>
            ))}
          </div>
        </section>

        <section className="py-12 text-center">
          <div className="rounded-xl border border-border bg-surface px-6 py-10 shadow-card max-w-lg mx-auto">
            <h2 className="font-serif text-2xl text-ink mb-2">Ready to try it?</h2>
            <p className="text-sm text-ink-muted mb-6">
              Bring a PDF resume and a job description you’re actually applying to.
            </p>
            <button
              onClick={() => navigate('/setup')}
              className="inline-flex items-center gap-2 px-5 py-2.5 rounded-lg bg-accent text-white text-sm font-medium hover:bg-blue-700 transition-colors"
            >
              Go to setup
              <ArrowRight size={16} />
            </button>
          </div>
        </section>
      </main>
    </div>
  )
}
