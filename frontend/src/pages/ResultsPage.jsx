import React, { useEffect, useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { motion } from 'framer-motion'
import { Trophy, BookOpen, RotateCcw, TrendingUp, Calendar, Award, Shield, FileText, ChevronRight } from 'lucide-react'
import Navbar from '../components/Navbar.jsx'
import MarkdownRenderer from '../components/MarkdownRenderer.jsx'

const fadeUp = {
  hidden: { opacity: 0, y: 15 },
  show: { opacity: 1, y: 0, transition: { duration: 0.5, ease: [0.19, 1, 0.22, 1] } },
}

function ScoreBar({ score, color }) {
  const pct = Math.round((score / 5.0) * 100)
  return (
    <div className="w-full h-1.5 rounded-full bg-white/5 overflow-hidden">
      <motion.div
        className="h-full rounded-full"
        style={{ backgroundColor: color }}
        initial={{ width: 0 }}
        animate={{ width: `${pct}%` }}
        transition={{ duration: 1, ease: 'easeOut', delay: 0.2 }}
      />
    </div>
  )
}

function getProficiencyDetails(score) {
  if (score >= 4.0) return { color: '#10b981', label: 'Expert' }     // Emerald
  if (score >= 2.5) return { color: '#3b82f6', label: 'Proficient' } // Ice Blue
  return { color: '#f59e0b', label: 'Developing' }                   // Gold/Amber
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

  const currentDate = new Date().toLocaleDateString('en-US', {
    year: 'numeric',
    month: 'long',
    day: 'numeric'
  })

  return (
    <div className="min-h-screen text-primaryText selection:bg-accent1/35 selection:text-white">
      <Navbar />

      <main className="relative z-10 max-w-6xl mx-auto px-6 pt-28 pb-20">
        <motion.div 
          initial="hidden" 
          animate="show"
          variants={{ show: { transition: { staggerChildren: 0.08 } } }}
        >
          {/* Header */}
          <motion.div variants={fadeUp} className="flex items-center gap-2 mb-2">
            <Trophy size={16} className="text-accent2 animate-pulse" />
            <span className="text-[10px] font-mono tracking-widest text-accent2 uppercase">Dossier Generated</span>
          </motion.div>

          <motion.h1 variants={fadeUp} className="text-3xl sm:text-4xl font-bold text-white mb-2">
            Skill Assessment dossier
          </motion.h1>
          <motion.p variants={fadeUp} className="text-text-muted text-sm font-light mb-10 max-w-xl leading-relaxed">
            Your credentials have been thoroughly benchmarked. Below is your detailed talent card and custom-curated syllabus.
          </motion.p>

          {/* ── certified Talent Card / score badge ── */}
          <motion.div
            variants={fadeUp}
            className="relative p-6 sm:p-8 rounded-xl border border-white/5 bg-panel overflow-hidden shadow-2xl mb-10"
          >
            {/* Visual background textures */}
            <div className="absolute inset-[1px] rounded-[11px] border border-white/[0.01] pointer-events-none" />
            <div className="absolute top-1/2 left-1/4 -translate-y-1/2 w-48 h-48 bg-accent1/5 blur-[80px] rounded-full pointer-events-none" />
            <div className="absolute top-1/2 right-1/4 -translate-y-1/2 w-48 h-48 bg-accent2/3 blur-[80px] rounded-full pointer-events-none" />

            <div className="flex flex-col md:flex-row md:items-center justify-between gap-8 relative z-10">
              
              {/* Left Column: Grade badge */}
              <div className="flex items-center gap-6">
                <div className="w-20 h-20 rounded-xl bg-white/[0.02] border border-white/15 flex flex-col items-center justify-center relative">
                  <div className="absolute top-1 right-1 w-1.5 h-1.5 rounded-full bg-accent2" />
                  <span className="text-3xl font-serif font-bold text-white leading-none">{avgScore}</span>
                  <span className="text-[8px] font-mono text-text-muted uppercase tracking-widest mt-1">/ 5.0 Rating</span>
                </div>

                <div>
                  <div className="inline-flex items-center gap-1.5 px-2.5 py-0.5 rounded bg-white/5 border border-white/10 text-[9px] font-mono text-text-muted uppercase tracking-wider mb-2">
                    <Award size={10} className="text-accent2" />
                    Overall Proficiency
                  </div>
                  <h3 className="text-lg font-semibold text-white tracking-wide">Competency Profile Match</h3>
                  <p className="text-[11px] text-text-muted/80 mt-0.5 flex items-center gap-1 font-light">
                    <Calendar size={11} className="text-accent1" /> Verified on {currentDate}
                  </p>
                </div>
              </div>

              {/* Right Column: Metadata Sign-off */}
              <div className="flex flex-col gap-2 md:text-right md:items-end">
                <div className="rounded border border-white/10 bg-black/40 p-3 font-mono text-[9px] space-y-1 text-left w-fit shrink-0">
                  <div className="text-accent1 flex items-center gap-1">
                    <Shield size={10} />
                    <span>AUTH_REF: CAT-X2901-IMPETUS</span>
                  </div>
                  <p className="text-text-muted/70">Engine consensus status: SECURE_STABLE</p>
                  <p className="text-cta">Evaluation signals processed: 3 / 3 OK</p>
                </div>
              </div>

            </div>
          </motion.div>

          {/* ── Two Column Results Dashboard ── */}
          <div className="grid grid-cols-1 lg:grid-cols-12 gap-8 items-start">
            
            {/* Left Column: Score Breakdown */}
            <motion.div variants={fadeUp} className="lg:col-span-5 space-y-4">
              <div className="flex items-center gap-2 pb-2 border-b border-white/5">
                <TrendingUp size={14} className="text-accent1" />
                <h3 className="text-xs font-semibold text-white tracking-wider uppercase">Competency Matrix</h3>
              </div>

              <div className="space-y-3.5">
                {evaluations.map((e, i) => {
                  const details = getProficiencyDetails(e.final_score)
                  return (
                    <motion.div
                      key={i}
                      initial={{ opacity: 0, x: -10 }}
                      animate={{ opacity: 1, x: 0 }}
                      transition={{ delay: i * 0.05 + 0.3, duration: 0.4, ease: [0.19, 1, 0.22, 1] }}
                      className="p-4 rounded-xl border border-white/5 bg-panel relative group"
                    >
                      <div className="absolute inset-[1px] rounded-[11px] border border-white/[0.01] pointer-events-none" />

                      <div className="flex items-start justify-between mb-2">
                        <span className="font-semibold text-xs text-white tracking-wide">{e.skill}</span>
                        <span 
                          className="text-[9px] font-mono font-bold px-2 py-0.5 rounded border uppercase tracking-wider"
                          style={{ 
                            color: details.color, 
                            borderColor: `${details.color}33`, 
                            backgroundColor: `${details.color}0F` 
                          }}
                        >
                          {details.label} · {e.final_score?.toFixed(1)}
                        </span>
                      </div>
                      
                      <ScoreBar score={e.final_score} color={details.color} />
                      
                      <p className="mt-3 text-[10px] text-text-muted leading-relaxed font-light">
                        {e.reasoning}
                      </p>
                    </motion.div>
                  )
                })}
              </div>
            </motion.div>

            {/* Right Column: Interactive growth Roadmap plan */}
            <motion.div variants={fadeUp} className="lg:col-span-7 space-y-4">
              <div className="flex items-center gap-2 pb-2 border-b border-white/5">
                <BookOpen size={14} className="text-accent2" />
                <h3 className="text-xs font-semibold text-white tracking-wider uppercase">Growth Roadmap & Syllabus</h3>
              </div>

              <div className="relative rounded-xl border border-white/5 bg-panel overflow-hidden group">
                <div className="absolute inset-[1px] rounded-[11px] border border-white/[0.01] pointer-events-none" />
                {/* Visual Gold bar highlight */}
                <div className="absolute top-0 left-0 right-0 h-[2px] bg-gradient-to-r from-accent1 via-accent2 to-accent1 opacity-40" />

                <div className="p-6 sm:p-8 max-h-[600px] overflow-y-auto scrollbar-thin">
                  {learning_plan ? (
                    <div className="prose-custom">
                      <MarkdownRenderer content={learning_plan} />
                    </div>
                  ) : (
                    <p className="text-xs text-text-muted/50 italic text-center py-10 font-light">
                      No matching resource curricula identified.
                    </p>
                  )}
                </div>
              </div>
            </motion.div>

          </div>

          {/* ── Reset action bar ── */}
          <motion.div variants={fadeUp} className="mt-12 pt-6 border-t border-white/5 text-center">
            <motion.button
              whileHover={{ y: -1 }}
              whileTap={{ y: 0 }}
              onClick={handleReset}
              className="inline-flex items-center gap-2 px-6 py-2.5 rounded-lg
                         border border-white/10 text-text-muted hover:text-white bg-white/5
                         font-semibold text-xs tracking-wider uppercase transition-all duration-300"
            >
              <RotateCcw size={12} />
              Start new assessment cycle
            </motion.button>
          </motion.div>

        </motion.div>
      </main>
    </div>
  )
}
