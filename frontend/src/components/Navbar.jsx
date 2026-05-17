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
                    bg-background/80 backdrop-blur-md border-b border-white/5">
      {/* Brand */}
      <Link to="/" className="flex items-center gap-2 group">
        <div className="w-8 h-8 rounded-lg bg-accent1/20 border border-accent1/40
                        flex items-center justify-center
                        group-hover:bg-accent1/30 transition-colors duration-300">
          <Zap size={16} className="text-accent1" />
        </div>
        <span className="text-primaryText font-semibold text-lg tracking-tight">
          Impetus
        </span>
      </Link>

      {/* Steps */}
      <div className="flex items-center gap-1">
        {steps.map((step, idx) => {
          const active = pathname === step.path
          return (
            <Link key={step.path} to={step.path}>
              <motion.div
                whileHover={{ scale: 1.04 }}
                whileTap={{ scale: 0.97 }}
                className={`relative px-4 py-1.5 rounded-full text-sm font-bold
                            transition-all duration-300
                            ${active
                              ? 'text-background bg-accent1 shadow-[0_0_15px_rgba(0,229,255,0.4)]'
                              : 'text-primaryText/40 hover:text-primaryText hover:bg-white/5'}`}
              >
                <span className="hidden sm:inline">{step.label}</span>
                <span className="sm:hidden">{idx + 1}</span>
              </motion.div>
            </Link>
          )
        })}
      </div>
    </nav>
  )
}
