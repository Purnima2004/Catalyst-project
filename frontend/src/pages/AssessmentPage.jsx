import React, { useState, useEffect, useRef } from 'react'
import { useNavigate } from 'react-router-dom'
import { motion, AnimatePresence } from 'framer-motion'
import { Send, Loader2, Bot, User, ChevronRight, CheckCircle2, Circle, PlayCircle, Terminal, HelpCircle } from 'lucide-react'
import Navbar from '../components/Navbar.jsx'
import { sendChat } from '../services/api.js'
import MarkdownRenderer from '../components/MarkdownRenderer.jsx'

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
    <div className="min-h-screen text-primaryText flex flex-col selection:bg-accent1/35 selection:text-white">
      <Navbar />

      {/* Main Workspace split */}
      <div className="flex-1 flex flex-col lg:flex-row pt-[60px] min-h-[calc(100vh-60px)]">
        
        {/* LEFT PANEL: Assessment Intelligence Sidebar */}
        <aside className="w-full lg:w-[320px] bg-panel border-b lg:border-b-0 lg:border-r border-white/5 flex flex-col shrink-0">
          {/* Top Progress block */}
          <div className="p-6 border-b border-white/5 space-y-4 relative">
            <div className="absolute inset-[1px] rounded-[11px] border border-white/[0.01] pointer-events-none" />
            
            <div className="flex justify-between items-center text-[10px] font-mono text-text-muted uppercase tracking-widest">
              <span>Overall Progress</span>
              <span>{progress}%</span>
            </div>

            <div className="h-1.5 rounded-full bg-white/5 overflow-hidden">
              <motion.div
                className="h-full rounded-full bg-gradient-to-r from-accent1 via-accent2 to-accent1"
                initial={{ width: 0 }}
                animate={{ width: `${progress}%` }}
                transition={{ duration: 0.8, ease: 'easeOut' }}
              />
            </div>
            
            <p className="text-[10px] text-text-muted/70 font-light">
              Assessing core competencies parsed from credentials.
            </p>
          </div>

          {/* Target Skills Checklist */}
          <div className="flex-1 p-6 space-y-4 overflow-y-auto">
            <h3 className="text-[10px] font-mono tracking-widest text-white uppercase font-semibold">Skill assessment matrix</h3>
            
            <div className="space-y-2">
              {skills_to_assess.map((skill, idx) => {
                const isAssessed = idx < current_skill_index
                const isActive = idx === current_skill_index
                const isPending = idx > current_skill_index

                return (
                  <div
                    key={skill}
                    className={`flex items-center gap-3 p-3 rounded-lg border transition-all duration-300
                      ${isActive 
                        ? 'bg-accent1/5 border-accent1/25 text-white' 
                        : isAssessed
                          ? 'bg-cta/[0.02] border-cta/15 text-cta/80'
                          : 'bg-white/[0.01] border-white/5 text-text-muted/50'}`}
                  >
                    <div className="shrink-0">
                      {isAssessed ? (
                        <CheckCircle2 size={13} className="text-cta" />
                      ) : isActive ? (
                        <PlayCircle size={13} className="text-accent1 animate-pulse" />
                      ) : (
                        <Circle size={13} className="text-text-muted/30" />
                      )}
                    </div>
                    <div className="min-w-0 flex-1">
                      <p className="text-xs font-semibold tracking-wide truncate">{skill}</p>
                      <p className="text-[9px] font-mono uppercase tracking-wider mt-0.5 opacity-60">
                        {isAssessed ? 'Assessed' : isActive ? 'Active Assessment' : 'Pending'}
                      </p>
                    </div>
                  </div>
                )
              })}
            </div>
          </div>
        </aside>

        {/* RIGHT PANEL: Conversation Timeline & Input */}
        <main className="flex-1 flex flex-col bg-background relative">
          
          {/* Scrollable Conversation timeline */}
          <div className="flex-1 overflow-y-auto px-6 pt-8 pb-32 max-w-3xl w-full mx-auto space-y-8">
            
            {/* Header info */}
            <div className="pb-4 border-b border-white/5 flex items-center justify-between text-xs text-text-muted/60">
              <div className="flex items-center gap-1.5 font-mono">
                <Terminal size={12} className="text-accent1" />
                <span>[session-active] evaluation terminal</span>
              </div>
              <span>Catalyst v1.4</span>
            </div>

            <AnimatePresence initial={false}>
              {messages.map((msg, i) => {
                const isAssistant = msg.role === 'assistant'
                return (
                  <motion.div
                    key={i}
                    initial={{ opacity: 0, y: 10 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ duration: 0.4, ease: [0.19, 1, 0.22, 1] }}
                    className="flex gap-4 items-start"
                  >
                    {/* Avatar icon */}
                    <div className={`shrink-0 w-8 h-8 rounded-lg flex items-center justify-center border font-mono text-[10px] font-bold mt-0.5
                      ${isAssistant
                        ? 'bg-panel border-white/10 text-accent2'
                        : 'bg-accent1/5 border-accent1/20 text-accent1'}`}
                    >
                      {isAssistant ? <Bot size={14} className="text-accent2" /> : <User size={14} className="text-accent1" />}
                    </div>

                    {/* Content Block */}
                    <div className="flex-1 space-y-1.5 min-w-0">
                      <div className="flex justify-between items-center text-[10px] font-mono text-text-muted">
                        <span className="uppercase font-semibold tracking-wider">
                          {isAssistant ? 'Assessor Engine' : 'Candidate'}
                        </span>
                        <span>{i === 0 ? 'Start' : `Msg #${i}`}</span>
                      </div>
                      
                      {/* Message Bubble container */}
                      <div className={`text-xs leading-relaxed font-light p-4 rounded-xl border
                        ${isAssistant
                          ? 'bg-panel border-white/5 text-white/90'
                          : 'bg-white/[0.01] border-white/5 text-white'}`}
                      >
                        <MarkdownRenderer content={msg.content} />
                      </div>
                    </div>
                  </motion.div>
                )
              })}
            </AnimatePresence>

            {/* Thinking evaluation indicator */}
            <AnimatePresence>
              {loading && (
                <motion.div 
                  initial={{ opacity: 0, y: 8 }} 
                  animate={{ opacity: 1, y: 0 }}
                  exit={{ opacity: 0 }} 
                  className="flex gap-4 items-start"
                >
                  <div className="w-8 h-8 rounded-lg bg-panel border border-white/10 flex items-center justify-center shrink-0 mt-0.5">
                    <Loader2 size={13} className="text-accent2 animate-spin" />
                  </div>
                  <div className="flex-1 space-y-1.5">
                    <div className="flex justify-between items-center text-[10px] font-mono text-text-muted">
                      <span className="uppercase font-semibold tracking-wider">Assessor Engine</span>
                      <span className="text-accent2 animate-pulse">Evaluating answer...</span>
                    </div>
                    <div className="p-4 rounded-xl border border-white/5 bg-panel text-xs text-text-muted/60 font-light flex items-center gap-2">
                      <Loader2 size={12} className="animate-spin text-accent1" />
                      Evaluating quantitative feedback and semantic skill match...
                    </div>
                  </div>
                </motion.div>
              )}
            </AnimatePresence>

            <div ref={bottomRef} />
          </div>

          {/* Typing Workspace Input bar */}
          <div className="absolute bottom-0 inset-x-0 bg-background/80 backdrop-blur-lg border-t border-white/5 p-4 z-20">
            <div className="max-w-3xl mx-auto flex gap-3 items-end">
              <div className="flex-1 relative border border-white/10 rounded-lg overflow-hidden bg-black/20 focus-within:border-accent1/40 transition-colors duration-300">
                <textarea
                  value={input}
                  onChange={(e) => setInput(e.target.value)}
                  onKeyDown={(e) => {
                    if (e.key === 'Enter' && !e.shiftKey) {
                      e.preventDefault()
                      sendMessage()
                    }
                  }}
                  rows={2}
                  placeholder="Type your structured answer here... Press Enter to submit"
                  disabled={loading}
                  className="w-full bg-transparent p-3 text-white text-xs leading-relaxed resize-none
                             placeholder-text-muted/40 outline-none font-light disabled:opacity-50"
                />
              </div>

              <motion.button
                whileHover={{ y: -1 }}
                whileTap={{ y: 0 }}
                onClick={sendMessage}
                disabled={!input.trim() || loading}
                className="w-10 h-10 rounded-lg bg-accent1 flex items-center justify-center shrink-0 border border-accent1
                           disabled:opacity-30 disabled:cursor-not-allowed hover:bg-accent1/90 transition-colors duration-200"
              >
                <Send size={14} className="text-white" />
              </motion.button>
            </div>
          </div>

        </main>
      </div>
    </div>
  )
}
