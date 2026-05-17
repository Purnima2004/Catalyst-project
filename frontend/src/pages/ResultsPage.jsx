import React, { useEffect, useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { motion } from 'framer-motion'
import { Trophy, BookOpen, RotateCcw, TrendingUp } from 'lucide-react'
import Navbar from '../components/Navbar.jsx'

const fadeUp = {
  hidden: { opacity: 0, y: 24 },
  show: { opacity: 1, y: 0, transition: { duration: 0.5, ease: 'easeOut' } },
}

function ScoreBar({ score, color }) {
  const pct = Math.round((score / 5.0) * 100)
  return (
    <div className="w-full h-1.5 rounded-full bg-white/8 overflow-hidden">
      <motion.div
        className="h-full rounded-full"
        style={{ backgroundColor: color }}
        initial={{ width: 0 }}
        animate={{ width: `${pct}%` }}
        transition={{ duration: 1, ease: 'easeOut', delay: 0.3 }}
      />
    </div>
  )
}

function getProficiencyColor(score) {
  if (score >= 3.5) return '#8bd6e9'  // accent1
  if (score >= 2.0) return '#e0b84d'  // amber
  return '#d23e8f'                     // accent2
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

  return (
    <div className="min-h-screen bg-background text-primaryText">
      <Navbar />

      {/* Glow */}
      <div className="pointer-events-none fixed inset-0 overflow-hidden">
        <div className="absolute top-0 right-1/4 w-[600px] h-[600px]
                        rounded-full bg-accent2/8 blur-[120px]" />
      </div>

      <main className="relative z-10 max-w-6xl mx-auto px-6 pt-28 pb-20">

        {/* ── Header ── */}
        <motion.div initial="hidden" animate="show"
          variants={{ show: { transition: { staggerChildren: 0.1 } } }}>

          <motion.div variants={fadeUp} className="flex items-center gap-3 mb-2">
            <Trophy size={20} className="text-accent1" />
            <p className="text-accent1 text-sm font-medium uppercase tracking-widest">Assessment Complete</p>
          </motion.div>

          <motion.h1 variants={fadeUp} className="text-4xl sm:text-5xl font-bold mb-3">
            Your Results
          </motion.h1>
          <motion.p variants={fadeUp} className="text-primaryText/50 text-lg mb-12">
            Here's a breakdown of your performance and a personalised learning plan to close your gaps.
          </motion.p>

          {/* ── Average Score Banner ── */}
          <motion.div
            variants={fadeUp}
            className="flex items-center gap-6 p-6 rounded-2xl border border-white/8
                       bg-white/3 mb-10"
          >
            <div className="text-center shrink-0">
              <p className="text-5xl font-bold text-transparent bg-clip-text
                             bg-gradient-to-br from-accent1 to-accent2">
                {avgScore}
              </p>
              <p className="text-xs text-primaryText/40 mt-1">/ 5.0 Average</p>
            </div>
            <div className="flex-1 h-px bg-white/8" />
            <div className="flex items-center gap-2 text-sm text-primaryText/50">
              <TrendingUp size={15} className="text-accent1" />
              {evaluations.length} skill{evaluations.length !== 1 ? 's' : ''} assessed
            </div>
          </motion.div>

          {/* ── Two Column Layout ── */}
          <div className="grid grid-cols-1 lg:grid-cols-5 gap-8">

            {/* Score Cards */}
            <motion.div variants={fadeUp} className="lg:col-span-2 space-y-4">
              <h2 className="text-xl font-semibold mb-4 flex items-center gap-2">
                <TrendingUp size={17} className="text-accent1" />
                Skill Breakdown
              </h2>
              {evaluations.map((e, i) => {
                const color = getProficiencyColor(e.final_score)
                const pct = Math.round((e.final_score / 5.0) * 100)
                return (
                  <motion.div
                    key={i}
                    initial={{ opacity: 0, x: -20 }}
                    animate={{ opacity: 1, x: 0 }}
                    transition={{ delay: i * 0.08 + 0.4, duration: 0.4 }}
                    className="p-5 rounded-2xl border border-white/8 bg-white/3
                               hover:border-white/15 transition-colors duration-200"
                  >
                    <div className="flex items-start justify-between mb-2">
                      <span className="font-medium text-sm text-primaryText">{e.skill}</span>
                      <span className="text-xs font-semibold shrink-0 ml-3"
                        style={{ color }}>
                        {e.proficiency} · {e.final_score?.toFixed(1)}/5
                      </span>
                    </div>
                    <ScoreBar score={e.final_score} color={color} />
                    <p className="mt-3 text-xs text-primaryText/40 leading-relaxed">
                      {e.reasoning}
                    </p>
                  </motion.div>
                )
              })}
            </motion.div>

            {/* Learning Plan */}
            <motion.div variants={fadeUp} className="lg:col-span-3">
              <h2 className="text-xl font-semibold mb-4 flex items-center gap-2">
                <BookOpen size={17} className="text-accent2" />
                Personalised Learning Plan
              </h2>
              <div className="p-7 rounded-2xl border border-white/8 bg-white/3
                              prose prose-invert prose-sm max-w-none
                              prose-headings:text-primaryText prose-headings:font-semibold
                              prose-p:text-primaryText/60 prose-p:leading-relaxed
                              prose-li:text-primaryText/60 prose-a:text-accent1">
                {learning_plan
                  ? <pre className="whitespace-pre-wrap font-sans text-sm text-primaryText/70 leading-relaxed">
                      {learning_plan}
                    </pre>
                  : <p className="text-primaryText/30 italic">No learning plan generated.</p>}
              </div>
            </motion.div>

          </div>

          {/* ── Restart ── */}
          <motion.div variants={fadeUp} className="mt-12 text-center">
            <motion.button
              whileHover={{ scale: 1.04 }}
              whileTap={{ scale: 0.97 }}
              onClick={handleReset}
              className="inline-flex items-center gap-2 px-8 py-3.5 rounded-xl
                         border border-white/10 text-primaryText/60 hover:text-primaryText
                         hover:border-white/25 font-medium text-sm transition-all duration-200"
            >
              <RotateCcw size={16} />
              Start a New Assessment
            </motion.button>
          </motion.div>

        </motion.div>
      </main>
    </div>
  )
}
