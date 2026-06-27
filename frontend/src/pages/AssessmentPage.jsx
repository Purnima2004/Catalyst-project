import React, { useState, useEffect, useRef } from 'react'
import { useNavigate } from 'react-router-dom'
import { Send, Loader2, CheckCircle2, Circle } from 'lucide-react'
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

  return (
    <div className="min-h-screen flex flex-col">
      <Navbar />

      <div className="flex-1 flex flex-col lg:flex-row pt-14 min-h-[calc(100vh-3.5rem)]">
        {/* Sidebar */}
        <aside className="w-full lg:w-64 border-b lg:border-b-0 lg:border-r border-border bg-surface shrink-0">
          <div className="p-5 border-b border-border">
            <p className="text-xs text-ink-faint mb-2">Progress</p>
            <div className="h-2 rounded-full bg-stone-100 overflow-hidden mb-1">
              <div
                className="h-full rounded-full bg-accent transition-all duration-500"
                style={{ width: `${progress}%` }}
              />
            </div>
            <p className="text-xs text-ink-muted">
              {current_skill_index} of {skills_to_assess.length} skills
            </p>
          </div>

          <div className="p-5">
            <p className="text-xs font-medium text-ink-muted uppercase tracking-wide mb-3">Skills</p>
            <ul className="space-y-2">
              {skills_to_assess.map((skill, idx) => {
                const done = idx < current_skill_index
                const active = idx === current_skill_index
                return (
                  <li
                    key={skill}
                    className={`flex items-center gap-2.5 text-sm rounded-lg px-2.5 py-2
                      ${active ? 'bg-accent-soft text-accent font-medium' : 'text-ink-muted'}`}
                  >
                    {done ? (
                      <CheckCircle2 size={15} className="text-success shrink-0" />
                    ) : (
                      <Circle size={15} className={`shrink-0 ${active ? 'text-accent' : 'text-stone-300'}`} />
                    )}
                    <span className="truncate">{skill}</span>
                  </li>
                )
              })}
            </ul>
          </div>
        </aside>

        {/* Chat */}
        <main className="flex-1 flex flex-col bg-background min-h-0">
          <div className="flex-1 overflow-y-auto px-5 py-6 max-w-2xl w-full mx-auto">
            {messages.length === 0 && (
              <p className="text-sm text-ink-muted text-center py-12">
                Your first question is loading…
              </p>
            )}

            <div className="space-y-6">
              {messages.map((msg, i) => {
                const isInterviewer = msg.role === 'assistant'
                return (
                  <div key={i} className={`flex ${isInterviewer ? 'justify-start' : 'justify-end'}`}>
                    <div
                      className={`max-w-[90%] rounded-2xl px-4 py-3 text-sm leading-relaxed
                        ${isInterviewer
                          ? 'bg-surface border border-border text-ink rounded-tl-sm shadow-card'
                          : 'bg-ink text-white rounded-tr-sm'}`}
                    >
                      {isInterviewer && (
                        <p className="text-xs font-medium text-ink-faint mb-1.5">Interviewer</p>
                      )}
                      <MarkdownRenderer content={msg.content} inverted={!isInterviewer} />
                    </div>
                  </div>
                )
              })}

              {loading && (
                <div className="flex justify-start">
                  <div className="bg-surface border border-border rounded-2xl rounded-tl-sm px-4 py-3 shadow-card">
                    <div className="flex items-center gap-2 text-sm text-ink-muted">
                      <Loader2 size={14} className="animate-spin text-accent" />
                      Reviewing your answer…
                    </div>
                  </div>
                </div>
              )}
            </div>
            <div ref={bottomRef} />
          </div>

          {/* Input */}
          <div className="border-t border-border bg-surface p-4">
            <div className="max-w-2xl mx-auto flex gap-2 items-end">
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
                placeholder="Type your answer… (Enter to send, Shift+Enter for new line)"
                disabled={loading}
                className="flex-1 rounded-lg border border-border-strong bg-stone-50/50 px-3 py-2.5 text-sm text-ink resize-none
                           placeholder:text-ink-faint outline-none focus:border-accent focus:ring-2 focus:ring-accent/10
                           disabled:opacity-50"
              />
              <button
                onClick={sendMessage}
                disabled={!input.trim() || loading}
                className="w-10 h-10 rounded-lg bg-accent text-white flex items-center justify-center shrink-0
                           hover:bg-blue-700 disabled:opacity-40 disabled:cursor-not-allowed transition-colors"
              >
                <Send size={16} />
              </button>
            </div>
          </div>
        </main>
      </div>
    </div>
  )
}
