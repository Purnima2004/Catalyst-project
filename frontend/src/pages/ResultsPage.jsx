import React, { useEffect, useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { RotateCcw } from 'lucide-react'
import Navbar from '../components/Navbar.jsx'
import MarkdownRenderer from '../components/MarkdownRenderer.jsx'

function ScoreBar({ score }) {
  const pct = Math.round((score / 5.0) * 100)
  const color = score >= 4 ? '#15803d' : score >= 2.5 ? '#1d4ed8' : '#b45309'
  return (
    <div className="h-1.5 rounded-full bg-stone-100 overflow-hidden">
      <div
        className="h-full rounded-full transition-all duration-700"
        style={{ width: `${pct}%`, backgroundColor: color }}
      />
    </div>
  )
}

function getProficiencyLabel(score) {
  if (score >= 4.0) return { label: 'Strong', color: 'text-success bg-success-soft' }
  if (score >= 2.5) return { label: 'Okay', color: 'text-accent bg-accent-soft' }
  return { label: 'Needs work', color: 'text-warn bg-warn-soft' }
}

export default function ResultsPage() {
  const navigate = useNavigate()
  const [state, setState] = useState(null)

  useEffect(() => {
    const saved = sessionStorage.getItem('catalyst_state')
    if (!saved) { navigate('/setup'); return }
    const parsed = JSON.parse(saved)
    if (!parsed.is_complete) { navigate('/assessment'); return }
    setState(parsed)
  }, [navigate])

  if (!state) return null

  const { evaluations = [], learning_plan = '' } = state
  const avgScore = evaluations.length
    ? (evaluations.reduce((s, e) => s + e.final_score, 0) / evaluations.length).toFixed(1)
    : 0

  const handleReset = () => {
    sessionStorage.clear()
    navigate('/setup')
  }

  const dateStr = new Date().toLocaleDateString('en-US', {
    year: 'numeric',
    month: 'long',
    day: 'numeric',
  })

  return (
    <div className="min-h-screen">
      <Navbar />

      <main className="max-w-4xl mx-auto px-5 pt-28 pb-20">
        <header className="mb-10">
          <p className="text-sm text-ink-muted mb-1">{dateStr}</p>
          <h1 className="text-2xl font-semibold text-ink mb-2">Your results</h1>
          <p className="text-sm text-ink-muted max-w-lg">
            Here’s how you did on each skill we tested, plus a learning plan based on the gaps.
          </p>
        </header>

        {/* Summary */}
        <div className="rounded-xl border border-border bg-surface p-6 shadow-card mb-8 flex items-center gap-6">
          <div className="text-center shrink-0">
            <p className="text-4xl font-semibold text-ink tabular-nums">{avgScore}</p>
            <p className="text-xs text-ink-muted mt-0.5">out of 5</p>
          </div>
          <div className="border-l border-border pl-6">
            <p className="text-sm font-medium text-ink mb-1">Overall</p>
            <p className="text-sm text-ink-muted leading-relaxed">
              Average across {evaluations.length} skill{evaluations.length !== 1 ? 's' : ''}.
              Scores are based on your interview answers — not just what’s on your resume.
            </p>
          </div>
        </div>

        <div className="grid lg:grid-cols-5 gap-8 items-start">
          {/* Scores */}
          <section className="lg:col-span-2 space-y-4">
            <h2 className="text-sm font-semibold text-ink">Skill breakdown</h2>
            {evaluations.map((e, i) => {
              const prof = getProficiencyLabel(e.final_score)
              return (
                <div key={i} className="rounded-xl border border-border bg-surface p-4 shadow-card">
                  <div className="flex items-start justify-between gap-2 mb-2">
                    <span className="text-sm font-medium text-ink">{e.skill}</span>
                    <span className={`text-xs font-medium px-2 py-0.5 rounded-full shrink-0 ${prof.color}`}>
                      {prof.label} · {e.final_score?.toFixed(1)}
                    </span>
                  </div>
                  <ScoreBar score={e.final_score} />
                  {e.reasoning && (
                    <p className="mt-3 text-xs text-ink-muted leading-relaxed">{e.reasoning}</p>
                  )}
                </div>
              )
            })}
          </section>

          {/* Learning plan */}
          <section className="lg:col-span-3">
            <h2 className="text-sm font-semibold text-ink mb-4">What to study next</h2>
            <div className="rounded-xl border border-border bg-surface p-6 shadow-card max-h-[640px] overflow-y-auto">
              {learning_plan ? (
                <MarkdownRenderer content={learning_plan} />
              ) : (
                <p className="text-sm text-ink-muted">No learning plan was generated.</p>
              )}
            </div>
          </section>
        </div>

        <div className="mt-12 pt-8 border-t border-border text-center">
          <button
            onClick={handleReset}
            className="inline-flex items-center gap-2 px-4 py-2 rounded-lg border border-border-strong text-sm text-ink-muted
                       hover:text-ink hover:bg-stone-50 transition-colors"
          >
            <RotateCcw size={14} />
            Try another job description
          </button>
        </div>
      </main>
    </div>
  )
}
