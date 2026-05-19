import React from 'react'
import { useNavigate } from 'react-router-dom'
import { motion } from 'framer-motion'
import { ArrowRight, BrainCircuit, BarChart3, BookOpen, Sparkles } from 'lucide-react'
import Navbar from '../components/Navbar.jsx'

const features = [
  {
    icon: BrainCircuit,
    title: 'Skill Knowledge Graph',
    desc: '50+ skills mapped with relationships. Deterministic gap analysis — no LLM hallucinations for skill identification.',
    color: 'accent1',
  },
  {
    icon: BarChart3,
    title: 'Hybrid Scoring Engine',
    desc: '3-signal evaluation: LLM qualitative score + semantic similarity + keyword coverage. Objective and explainable.',
    color: 'accent2',
  },
  {
    icon: BookOpen,
    title: 'RAG Resource Curator',
    desc: 'Learning plan grounded in 35+ real, curated resources. No hallucinated links — ever.',
    color: 'cta',
  },
]

const containerVariants = {
  hidden: {},
  show: { transition: { staggerChildren: 0.15 } },
}

const fadeUp = {
  hidden: { opacity: 0, y: 32 },
  show: { opacity: 1, y: 0, transition: { duration: 0.6, ease: 'easeOut' } },
}

export default function LandingPage() {
  const navigate = useNavigate()

  return (
    <div className="min-h-screen text-primaryText overflow-hidden relative">
      <Navbar />

      {/* ── Background Depth ── */}
      <div className="pointer-events-none absolute inset-0">
      </div>

      <Navbar />

      {/* ── Hero ── */}
      <section className="relative flex flex-col items-center justify-center
                          min-h-screen px-6 text-center pt-24">

        <motion.div
          variants={containerVariants}
          initial="hidden"
          animate="show"
          className="relative z-10 max-w-4xl"
        >


          {/* Headline */}
          <motion.h1
            variants={fadeUp}
            className="text-5xl sm:text-6xl md:text-7xl font-bold tracking-tight
                       leading-[1.1] mb-6"
          >
            What's holding you back?{' '}
            <span className="text-transparent bg-clip-text
                             bg-gradient-to-r from-cyan-400 to-fuchsia-400">
              Let's find out.
            </span>
          </motion.h1>

          {/* Sub */}
          <motion.p
            variants={fadeUp}
            className="text-primaryText/60 text-lg sm:text-xl max-w-2xl mx-auto mb-10 leading-relaxed"
          >
            Impetus analyses your résumé against any job description, conducts a
            personalised AI interview, and generates a curated learning plan — in minutes.
          </motion.p>

          {/* CTA */}
          <motion.div variants={fadeUp} className="flex flex-col sm:flex-row gap-4 justify-center">
            <motion.button
              whileHover={{
                scale: 1.05,
                boxShadow: '0 0 40px rgba(99,64,255,0.4)'
              }}
              whileTap={{ scale: 0.97 }}
              onClick={() => navigate('/setup')}
              className="inline-flex items-center gap-2 px-8 py-3.5 rounded-xl
                         bg-accent1 text-white font-bold text-lg
                         shadow-[0_0_20px_rgba(99,64,255,0.2)]
                         transition-all duration-300 hover:brightness-110"
            >
              Start Your Assessment
              <ArrowRight size={20} />
            </motion.button>

            <motion.button
              whileHover={{ scale: 1.04 }}
              whileTap={{ scale: 0.97 }}
              className="inline-flex items-center gap-2 px-8 py-3.5 rounded-xl
                         border border-white/10 text-primaryText/70 hover:text-primaryText
                         hover:border-white/20 font-medium text-base transition-colors duration-200"
            >
              View Demo
            </motion.button>
          </motion.div>
        </motion.div>

        {/* Scroll hint */}
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1, y: [0, 8, 0] }}
          transition={{ delay: 1.4, duration: 2, repeat: Infinity }}
          className="absolute bottom-8 left-1/2 -translate-x-1/2
                     w-5 h-8 rounded-full border border-white/20
                     flex items-start justify-center pt-1.5"
        >
          <div className="w-1 h-2 rounded-full bg-white/40" />
        </motion.div>
      </section>

      {/* ── Feature Cards ── */}
      <section className="relative px-6 py-28 max-w-6xl mx-auto">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          transition={{ duration: 0.6 }}
          className="text-center mb-16"
        >
          <h2 className="text-3xl sm:text-4xl font-bold mb-4">
            How Impetus works
          </h2>
          <p className="text-primaryText/50 text-lg max-w-xl mx-auto">
            Three intelligent systems working in concert to give you a completely objective picture.
          </p>
        </motion.div>

        <motion.div
          variants={containerVariants}
          initial="hidden"
          whileInView="show"
          viewport={{ once: true }}
          className="grid grid-cols-1 md:grid-cols-3 gap-6"
        >
          {features.map(({ icon: Icon, title, desc, color }) => (
            <motion.div
              key={title}
              variants={fadeUp}
              whileHover={{ y: -6, transition: { duration: 0.25 } }}
              className="group relative p-7 rounded-2xl border border-white/8
                         bg-white/3 backdrop-blur-sm
                         hover:border-white/15 transition-colors duration-300"
            >
              {/* Icon */}
              <div className={`w-11 h-11 rounded-xl mb-5 flex items-center justify-center
                bg-${color}/15 border border-${color}/25
                group-hover:bg-${color}/25 transition-colors duration-300`}>
                <Icon size={20} className={`text-${color}`} />
              </div>
              <h3 className="text-lg font-semibold text-primaryText mb-2">{title}</h3>
              <p className="text-primaryText/50 text-sm leading-relaxed">{desc}</p>
            </motion.div>
          ))}
        </motion.div>
      </section>

      {/* ── Bottom CTA ── */}
      <section className="px-6 py-24 text-center">
        <motion.div
          initial={{ opacity: 0, scale: 0.96 }}
          whileInView={{ opacity: 1, scale: 1 }}
          viewport={{ once: true }}
          transition={{ duration: 0.6 }}
          className="max-w-2xl mx-auto p-12 rounded-3xl border border-white/8
                     bg-gradient-to-br from-accent1/10 to-accent2/10"
        >
          <h2 className="text-3xl font-bold mb-4">Ready to close your skill gaps?</h2>
          <p className="text-primaryText/50 mb-8">
            Upload your resume, paste a job description, and let Impetus do the rest.
          </p>
          <motion.button
            whileHover={{ scale: 1.05, boxShadow: '0 0 32px rgba(99,64,255,0.5)' }}
            whileTap={{ scale: 0.97 }}
            onClick={() => navigate('/setup')}
            className="inline-flex items-center gap-2 px-8 py-3.5 rounded-xl
                       bg-accent1 text-white font-semibold transition-shadow duration-300"
          >
            Get Started <ArrowRight size={18} />
          </motion.button>
        </motion.div>
      </section>
    </div>
  )
}
