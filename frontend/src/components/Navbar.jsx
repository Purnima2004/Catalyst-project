import React from 'react'
import { Link, useLocation } from 'react-router-dom'
import { motion } from 'framer-motion'
import { Zap } from 'lucide-react'

const steps = [
  { label: 'Home',       path: '/' },
  { label: 'Setup',      path: '/setup' },
  { label: 'Assessment', path: '/assessment' },
  { label: 'Results',    path: '/results' },
]

export default function Navbar() {
  const { pathname } = useLocation()

  return (
    <nav className="fixed top-0 inset-x-0 z-50 flex items-center justify-between px-8 py-4
                    bg-background/70 backdrop-blur-lg border-b border-border-subtle">
      {/* Brand */}
      <Link to="/" className="flex items-center gap-2.5 group">
        <div className="w-6 h-6 rounded-md bg-panel border border-white/10
                        flex items-center justify-center transition-all duration-300
                        group-hover:border-accent1/50">
          <Zap size={12} className="text-accent1 group-hover:scale-110 transition-transform duration-300" />
        </div>
        <span className="text-white font-medium text-sm tracking-[0.25em] uppercase transition-all duration-300 group-hover:text-accent1">
          Impetus<span className="text-accent2 font-bold font-serif">.</span>
        </span>
      </Link>

      {/* Steps */}
      <div className="flex items-center gap-1">
        {steps.map((step, idx) => {
          const active = pathname === step.path
          return (
            <Link key={step.path} to={step.path}>
              <motion.div
                whileHover={{ y: -0.5 }}
                whileTap={{ y: 0 }}
                className={`relative px-4 py-1 text-[11px] font-mono tracking-widest uppercase transition-all duration-300 cursor-pointer
                            ${active
                              ? 'text-white font-medium'
                              : 'text-text-muted/60 hover:text-white'}`}
              >
                <span>{step.label}</span>
                {active && (
                  <motion.div 
                    layoutId="activeTabBorder"
                    className="absolute bottom-[-17px] left-3 right-3 h-[1px] bg-accent2"
                    transition={{ type: 'spring', stiffness: 380, damping: 30 }}
                  />
                )}
              </motion.div>
            </Link>
          )
        })}
      </div>
    </nav>
  )
}
