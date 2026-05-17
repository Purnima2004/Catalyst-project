import React, { useState, useEffect, useRef } from 'react'
import { useNavigate } from 'react-router-dom'
import { motion, AnimatePresence } from 'framer-motion'
import { Send, Loader2, Bot, User, ChevronRight } from 'lucide-react'
import Navbar from '../components/Navbar.jsx'
import { sendChat } from '../services/api.js'

export default function AssessmentPage() {
  const navigate = useNavigate()
  const [state, setState] = useState(null)
  const [threadId, setThreadId] = useState(null)
  const [input, setInput] = useState('')
  const [loading, setLoading] = useState(false)
  const bottomRef = useRef(null)

  useEffect(() => {
    const tid = sessionStorage.getItem('catalyst_thread_id')
    const savedState = sessionStorage.getItem('catalyst_state')
    if (!tid || !savedState) { navigate('/setup'); return }
    setThreadId(tid)
    setState(JSON.parse(savedState))
  }, [navigate])

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: 'smooth' })
  }, [state?.messages])

  const sendMessage = async () => {
    if (!input.trim() || loading) return
    const userMsg = input.trim()
    setInput('')
    setLoading(true)

    // Optimistically add user message
    setState(prev => ({
      ...prev,
      messages: [...(prev?.messages || []), { role: 'user', content: userMsg }],
    }))

    try {
      const result = await sendChat({ thread_id: threadId, message: userMsg })
      setState(result)
      sessionStorage.setItem('catalyst_state', JSON.stringify(result))
      if (result.is_complete) {
        navigate('/results')
      }
    } catch (e) {
      console.error(e)
    } finally {
      setLoading(false)
    }
  }

  if (!state) return null

  const { messages = [], skills_to_assess = [], current_skill_index = 0 } = state
  const progress = skills_to_assess.length > 0
    ? Math.round((current_skill_index / skills_to_assess.length) * 100)
    : 0
  const currentSkill = skills_to_assess[current_skill_index]

  return (
    <div className="min-h-screen bg-background text-primaryText flex flex-col">
      <Navbar />

      {/* Fixed progress bar under navbar */}
      <div className="fixed top-[65px] inset-x-0 z-40 bg-background border-b border-white/5 px-6 py-3">
        <div className="max-w-3xl mx-auto flex items-center gap-4">
          <div className="flex-1 h-1.5 rounded-full bg-white/8 overflow-hidden">
            <motion.div
              className="h-full rounded-full bg-gradient-to-r from-accent1 to-accent2"
              initial={{ width: 0 }}
              animate={{ width: `${progress}%` }}
              transition={{ duration: 0.8, ease: 'easeOut' }}
            />
          </div>
          <span className="text-xs text-primaryText/40 whitespace-nowrap shrink-0">
            Skill {current_skill_index} of {skills_to_assess.length}
          </span>
          {currentSkill && (
            <span className="hidden sm:flex items-center gap-1.5 text-xs px-3 py-1
                             rounded-full bg-accent1/15 text-accent1 border border-accent1/25">
              <ChevronRight size={12} />
              {currentSkill}
            </span>
          )}
        </div>
      </div>

      {/* Chat area */}
      <main className="flex-1 max-w-3xl w-full mx-auto px-4 pt-36 pb-36">
        <AnimatePresence initial={false}>
          {messages.map((msg, i) => (
            <motion.div
              key={i}
              initial={{ opacity: 0, y: 16 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.35, ease: 'easeOut' }}
              className={`flex gap-3 mb-6 ${msg.role === 'user' ? 'flex-row-reverse' : ''}`}
            >
              {/* Avatar */}
              <div className={`shrink-0 w-8 h-8 rounded-full flex items-center justify-center
                ${msg.role === 'assistant'
                  ? 'bg-accent1/20 border border-accent1/30'
                  : 'bg-accent2/20 border border-accent2/30'}`}>
                {msg.role === 'assistant'
                  ? <Bot size={15} className="text-accent1" />
                  : <User size={15} className="text-accent2" />}
              </div>

              {/* Bubble */}
              <div className={`max-w-[78%] px-5 py-3.5 rounded-2xl text-sm leading-relaxed
                ${msg.role === 'assistant'
                  ? 'bg-white/5 border border-white/8 text-primaryText rounded-tl-sm'
                  : 'bg-accent2/15 border border-accent2/20 text-primaryText rounded-tr-sm'}`}>
                {msg.content}
              </div>
            </motion.div>
          ))}
        </AnimatePresence>

        {/* Thinking indicator */}
        <AnimatePresence>
          {loading && (
            <motion.div initial={{ opacity: 0, y: 12 }} animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0 }} className="flex gap-3 mb-6">
              <div className="w-8 h-8 rounded-full bg-accent1/20 border border-accent1/30
                              flex items-center justify-center">
                <Bot size={15} className="text-accent1" />
              </div>
              <div className="px-5 py-3.5 rounded-2xl rounded-tl-sm bg-white/5
                              border border-white/8 flex items-center gap-2">
                <Loader2 size={14} className="text-accent1 animate-spin" />
                <span className="text-sm text-primaryText/50">Evaluating your answer…</span>
              </div>
            </motion.div>
          )}
        </AnimatePresence>

        <div ref={bottomRef} />
      </main>

      {/* Fixed input bar */}
      <div className="fixed bottom-0 inset-x-0 bg-background/90 backdrop-blur-md
                      border-t border-white/5 px-4 py-4 z-40">
        <div className="max-w-3xl mx-auto flex gap-3">
          <input
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={(e) => e.key === 'Enter' && !e.shiftKey && sendMessage()}
            placeholder="Type your answer and press Enter…"
            disabled={loading}
            className="flex-1 bg-white/5 border border-white/10 rounded-xl px-5 py-3.5
                       text-primaryText text-sm placeholder-primaryText/25
                       outline-none focus:border-accent1/40 focus:bg-white/8
                       transition-all duration-200 disabled:opacity-40"
          />
          <motion.button
            whileHover={{ scale: 1.05 }}
            whileTap={{ scale: 0.95 }}
            onClick={sendMessage}
            disabled={!input.trim() || loading}
            className="w-12 h-12 rounded-xl bg-accent1 flex items-center justify-center
                       disabled:opacity-30 disabled:cursor-not-allowed
                       hover:bg-accent1/80 transition-colors duration-200"
          >
            <Send size={17} className="text-background" />
          </motion.button>
        </div>
      </div>
    </div>
  )
}
