import React from 'react'
import { useNavigate } from 'react-router-dom'
import { motion } from 'framer-motion'
import { ArrowRight, BrainCircuit, BarChart3, BookOpen, Sparkles, Terminal, Shield, CheckCircle, Zap } from 'lucide-react'
import Navbar from '../components/Navbar.jsx'

const features = [
  {
    icon: BrainCircuit,
    title: 'Skill Knowledge Graph',
    desc: '50+ skills mapped with rich structural relationships. Deterministic gap analysis — no LLM hallucinations for core skill identification.',
    color: 'accent1', // maps to Ice Blue
    borderColor: 'border-accent1/20',
    iconColor: 'text-accent1',
    bgColor: 'bg-accent1/5'
  },
  {
    icon: BarChart3,
    title: 'Hybrid Scoring Engine',
    desc: '3-signal evaluation combining qualitative critique, semantic similarity, and dense keyword coverage. Objective, auditable, and deep.',
    color: 'accent2', // maps to Gold
    borderColor: 'border-accent2/20',
    iconColor: 'text-accent2',
    bgColor: 'bg-accent2/5'
  },
  {
    icon: BookOpen,
    title: 'RAG Resource Curator',
    desc: 'Bespoke learning plan grounded in 35+ verified, real-world educational resources. No hallucinated links or fake textbooks.',
    color: 'cta', // maps to Emerald
    borderColor: 'border-cta/20',
    iconColor: 'text-cta',
    bgColor: 'bg-cta/5'
  },
]

const containerVariants = {
  hidden: {},
  show: { transition: { staggerChildren: 0.1 } },
}

const fadeUp = {
  hidden: { opacity: 0, y: 20 },
  show: { opacity: 1, y: 0, transition: { duration: 0.5, ease: [0.19, 1, 0.22, 1] } },
}

export default function LandingPage() {
  const navigate = useNavigate()

  return (
    <div className="min-h-screen text-primaryText overflow-hidden relative selection:bg-accent1/35 selection:text-white">
      <Navbar />

      {/* Hero Section */}
      <section className="relative min-h-screen flex items-center justify-center pt-28 pb-16 px-6 max-w-6xl mx-auto">
        <div className="grid grid-cols-1 lg:grid-cols-12 gap-12 items-center w-full">
          
          {/* Left: Text Content */}
          <motion.div
            variants={containerVariants}
            initial="hidden"
            animate="show"
            className="lg:col-span-7 flex flex-col justify-center text-left"
          >
            {/* Editorial Typographic Heading */}
            <motion.h1
              variants={fadeUp}
              className="text-4xl sm:text-5xl md:text-6.5xl font-extralight leading-[1.15] tracking-tight text-white mb-6"
            >
              What is holding your career <span className="font-serif italic font-light text-accent2">back?</span>
              <br />
              <span className="font-medium text-white/95">Let's find out.</span>
            </motion.h1>

            {/* Subtle Tagline */}
            <motion.p
              variants={fadeUp}
              className="text-text-muted text-sm sm:text-base max-w-lg mb-10 leading-relaxed font-light"
            >
              Impetus analyses your résumé against any job description, conducts a 
              hyper-personalised AI interview, and generates a structured, resource-grounded learning plan in minutes.
            </motion.p>

            {/* Premium Minimal CTA Buttons */}
            <motion.div variants={fadeUp} className="flex flex-col sm:flex-row gap-4">
              <motion.button
                whileHover={{ y: -1 }}
                whileTap={{ y: 0 }}
                onClick={() => navigate('/setup')}
                className="inline-flex items-center justify-center gap-2 px-6 py-3 rounded
                           bg-white hover:bg-slate-100 text-black font-semibold text-xs tracking-wider uppercase
                           shadow-sm transition-all duration-300 border border-white hover:border-slate-100"
              >
                Start Assessment
                <ArrowRight size={14} />
              </motion.button>

              <motion.button
                whileHover={{ y: -1 }}
                whileTap={{ y: 0 }}
                className="inline-flex items-center justify-center gap-2 px-6 py-3 rounded
                           border border-white/10 text-white hover:text-white hover:border-white/20
                           font-semibold text-xs tracking-wider uppercase bg-white/[0.02] transition-all duration-300"
              >
                View Architecture
              </motion.button>
            </motion.div>
          </motion.div>

          {/* Right: Premium Minimalist Dashboard Mock */}
          <motion.div
            initial={{ opacity: 0, x: 30 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ duration: 0.8, ease: [0.19, 1, 0.22, 1], delay: 0.2 }}
            className="lg:col-span-5"
          >
            <div className="relative rounded-2xl border border-white/[0.04] bg-panel/40 backdrop-blur-md p-6 shadow-2xl overflow-hidden group">
              {/* Double border highlight */}
              <div className="absolute inset-[1px] rounded-[15px] border border-white/[0.01] pointer-events-none" />

              {/* Top Bar */}
              <div className="flex items-center justify-between pb-3.5 border-b border-white/[0.04] mb-4">
                <div className="flex items-center gap-2">
                  <div className="w-1.5 h-1.5 rounded-full bg-accent1 animate-pulse" />
                  <span className="text-[9px] font-mono tracking-widest text-text-muted/80 uppercase font-medium">Assessment dossier</span>
                </div>
                <span className="text-[8px] font-mono px-2 py-0.5 rounded bg-white/5 text-accent2 border border-white/5">CAT-ID-9082</span>
              </div>

              {/* Content Grid */}
              <div className="space-y-4">
                
                {/* Candidate Overview Card */}
                <div className="p-3 bg-white/[0.01] border border-white/[0.03] rounded-lg flex items-center justify-between">
                  <div>
                    <h4 className="text-xs font-semibold text-white tracking-wide">Alexander Chen</h4>
                    <p className="text-[9px] text-text-muted/70 font-mono uppercase tracking-widest mt-0.5">Systems Architect</p>
                  </div>
                  <div className="text-right">
                    <span className="text-xs font-serif font-semibold text-accent2">4.7 <span className="text-[9px] text-text-muted">/ 5.0</span></span>
                    <p className="text-[8px] text-cta font-mono uppercase tracking-widest mt-0.5">Top 3% Match</p>
                  </div>
                </div>

                {/* Skill Graph Bar Chart */}
                <div className="space-y-3.5 pt-1">
                  
                  {/* Skill 1 */}
                  <div className="space-y-1.5">
                    <div className="flex justify-between text-[10px] font-medium text-white/95">
                      <span className="tracking-wide font-light">Distributed Systems (Consensus)</span>
                      <span className="text-accent1 font-mono text-[9px]">92%</span>
                    </div>
                    <div className="h-[2px] bg-white/5 rounded-full overflow-hidden">
                      <div className="h-full bg-accent1 rounded-full w-[92%]" />
                    </div>
                  </div>

                  {/* Skill 2 */}
                  <div className="space-y-1.5">
                    <div className="flex justify-between text-[10px] font-medium text-white/95">
                      <span className="tracking-wide font-light">Architectural Safety & Verification</span>
                      <span className="text-accent2 font-mono text-[9px]">86%</span>
                    </div>
                    <div className="h-[2px] bg-white/5 rounded-full overflow-hidden">
                      <div className="h-full bg-accent2 rounded-full w-[86%]" />
                    </div>
                  </div>

                  {/* Skill 3 */}
                  <div className="space-y-1.5">
                    <div className="flex justify-between text-[10px] font-medium text-white/95">
                      <span className="tracking-wide font-light">Go Concurrency & Channels</span>
                      <span className="text-cta font-mono text-[9px]">79%</span>
                    </div>
                    <div className="h-[2px] bg-white/5 rounded-full overflow-hidden">
                      <div className="h-full bg-cta rounded-full w-[79%]" />
                    </div>
                  </div>

                </div>

                {/* Console Log */}
                <div className="rounded-lg bg-black/30 p-4 border border-white/[0.03] font-mono text-[9px] space-y-2 leading-relaxed text-slate-400">
                  <div className="text-accent1 flex items-center gap-1.5 font-semibold">
                    <Terminal size={10} className="shrink-0 text-accent1" />
                    <span className="tracking-widest uppercase text-[8px] text-text-muted/65">[impetus-engine] analyzing payload</span>
                  </div>
                  <p className="text-white/60 font-light italic leading-normal">"Demonstrated strong qualitative reasoning on write path guarantees under partitioning conditions."</p>
                  <div className="text-cta flex items-center gap-1 mt-1 text-[8px] uppercase tracking-widest font-semibold font-mono">
                    <Shield size={9} />
                    <span>✓ Signal consensus validated</span>
                  </div>
                </div>

              </div>
            </div>
          </motion.div>
        </div>
      </section>

      {/* How it Works / Feature Section */}
      <section className="relative px-6 py-24 max-w-6xl mx-auto border-t border-white/5">
        <motion.div
          initial={{ opacity: 0, y: 15 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          transition={{ duration: 0.5 }}
          className="text-left mb-16 max-w-xl"
        >
          <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full border border-white/10 bg-white/5 mb-4">
            <span className="text-[9px] font-mono tracking-widest text-text-muted uppercase">Architecture breakdown</span>
          </div>
          <h2 className="text-3xl font-bold mb-3 text-white">
            Structured Objective Evaluation
          </h2>
          <p className="text-text-muted text-base font-light leading-relaxed">
            Three core sub-systems operating in concert to paint a completely unbiased, deep picture of developer capability.
          </p>
        </motion.div>

        <motion.div
          variants={containerVariants}
          initial="hidden"
          whileInView="show"
          viewport={{ once: true }}
          className="grid grid-cols-1 md:grid-cols-3 gap-6"
        >
          {features.map(({ icon: Icon, title, desc, iconColor, borderColor, bgColor }) => (
            <motion.div
              key={title}
              variants={fadeUp}
              whileHover={{ y: -3 }}
              transition={{ duration: 0.3, ease: 'easeOut' }}
              className="relative p-7 rounded-xl border border-white/5 bg-panel hover:bg-panel-hover transition-all duration-300"
            >
              {/* Double border highlight */}
              <div className="absolute inset-[1px] rounded-[11px] border border-white/[0.01] pointer-events-none" />

              {/* Custom-styled Monocolor Icon */}
              <div className={`w-10 h-10 rounded-lg mb-5 flex items-center justify-center ${bgColor} border ${borderColor}`}>
                <Icon size={18} className={iconColor} />
              </div>
              <h3 className="text-base font-semibold text-white tracking-wide mb-2">{title}</h3>
              <p className="text-text-muted text-xs leading-relaxed font-light">{desc}</p>
            </motion.div>
          ))}
        </motion.div>
      </section>

      {/* Premium CTA Bottom Card */}
      <section className="px-6 py-20 max-w-6xl mx-auto border-t border-white/5">
        <motion.div
          initial={{ opacity: 0, scale: 0.98 }}
          whileInView={{ opacity: 1, scale: 1 }}
          viewport={{ once: true }}
          transition={{ duration: 0.6, ease: [0.19, 1, 0.22, 1] }}
          className="relative p-12 rounded-2xl border border-white/5 bg-panel overflow-hidden text-center max-w-3xl mx-auto"
        >
          <div className="absolute inset-0 bg-[radial-gradient(circle_at_center,rgba(59,130,246,0.03)_0%,transparent_100%)] pointer-events-none" />
          <div className="absolute inset-[1px] rounded-[15px] border border-white/[0.02] pointer-events-none" />

          <h2 className="text-2xl sm:text-3xl font-bold text-white mb-3">Ready to evaluate your skill gap?</h2>
          <p className="text-text-muted text-sm font-light max-w-lg mx-auto mb-8">
            Upload your resume, paste your target job description, and let Impetus deliver an in-depth technical dossier.
          </p>
          <motion.button
            whileHover={{ y: -2 }}
            whileTap={{ y: 0 }}
            onClick={() => navigate('/setup')}
            className="inline-flex items-center gap-2 px-7 py-3 rounded-lg
                       bg-accent1 hover:bg-accent1/95 text-white font-semibold text-xs tracking-wider uppercase
                       shadow-[0_4px_20px_rgba(59,130,246,0.15)] border border-accent1 transition-all duration-300"
          >
            Get Started <ArrowRight size={14} />
          </motion.button>
        </motion.div>
      </section>
    </div>
  )
}
