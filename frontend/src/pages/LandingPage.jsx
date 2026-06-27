import React from 'react'
import { useNavigate } from 'react-router-dom'
import { ArrowRight, FileText, MessageSquare, ListChecks } from 'lucide-react'
import Navbar from '../components/Navbar.jsx'
import GradientBackground from '../components/GradientBackground.jsx'

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

      {/* Hero — full viewport animated gradient */}
      <section className="relative min-h-screen flex items-center justify-center px-5 pt-14">
        <GradientBackground />

        <div className="relative z-10 max-w-2xl mx-auto text-center py-20">
          <p className="text-sm text-ink-muted mb-5">For developers prepping for a specific role</p>
          <h1 className="font-serif text-4xl sm:text-5xl md:text-[3.25rem] leading-[1.12] text-ink mb-6">
            Find the gap between your resume and the job.
          </h1>
          <p className="text-[15px] sm:text-base text-ink-muted leading-relaxed mb-10 max-w-lg mx-auto">
            Impetus reads your resume next to a job description, runs a quick technical
            interview on the skills that matter, and tells you what to work on next.
          </p>
          <div className="flex flex-wrap items-center justify-center gap-3">
            <button
              onClick={() => navigate('/setup')}
              className="inline-flex items-center gap-2 px-6 py-3 rounded-lg bg-ink text-white text-sm font-medium hover:bg-stone-800 transition-colors shadow-lift"
            >
              Start free
              <ArrowRight size={16} />
            </button>
            <a
              href="https://github.com/Purnima2004/Impetus-project"
              target="_blank"
              rel="noreferrer"
              className="inline-flex items-center px-6 py-3 rounded-lg border border-white/60 bg-white/40 backdrop-blur-sm text-sm font-medium text-ink-muted hover:text-ink hover:bg-white/60 transition-colors"
            >
              View on GitHub
            </a>
          </div>
        </div>
      </section>

      <main className="relative z-10 bg-background">
        <section className="max-w-5xl mx-auto px-5 py-20 border-t border-border">
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

        <section className="max-w-5xl mx-auto px-5 pb-20 text-center">
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
