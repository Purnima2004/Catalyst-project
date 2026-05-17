import React, { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { motion, AnimatePresence } from 'framer-motion'
import { Upload, FileText, Briefcase, ArrowRight, CheckCircle, AlertCircle, Loader2 } from 'lucide-react'
import Navbar from '../components/Navbar.jsx'
import { uploadResume, startAssessment } from '../services/api.js'

const fadeUp = {
  hidden: { opacity: 0, y: 24 },
  show: { opacity: 1, y: 0, transition: { duration: 0.5, ease: 'easeOut' } },
}

export default function SetupPage() {
  const navigate = useNavigate()
  const [resumeFile, setResumeFile] = useState(null)
  const [jobDescription, setJobDescription] = useState('')
  const [dragging, setDragging] = useState(false)
  const [status, setStatus] = useState('idle') // idle | uploading | starting | error
  const [errorMsg, setErrorMsg] = useState('')
  const [resumeData, setResumeData] = useState(null)

  const handleFileDrop = (e) => {
    e.preventDefault()
    setDragging(false)
    const file = e.dataTransfer?.files[0] || e.target.files[0]
    if (file && file.type === 'application/pdf') setResumeFile(file)
  }

  const handleUpload = async (file) => {
    setResumeFile(file)
    setStatus('uploading')
    try {
      const data = await uploadResume(file)
      setResumeData(data)
      setStatus('idle')
    } catch {
      setErrorMsg('Failed to upload resume. Is the backend running?')
      setStatus('error')
    }
  }

  const handleStart = async () => {
    if (!resumeData || !jobDescription.trim()) return
    setStatus('starting')
    try {
      const result = await startAssessment({
        job_description: jobDescription,
        resume_hash: resumeData.resume_hash,
        resume_text: resumeData.resume_text,
        is_returning_user: resumeData.is_returning_user,
      })
      // Store thread_id so Assessment page can pick it up
      sessionStorage.setItem('catalyst_thread_id', result.thread_id)
      sessionStorage.setItem('catalyst_state', JSON.stringify(result))
      navigate('/assessment')
    } catch {
      setErrorMsg('Failed to start assessment. Please try again.')
      setStatus('error')
    }
  }

  const canStart = resumeData && jobDescription.trim().length > 50 && status === 'idle'

  return (
    <div className="min-h-screen bg-background text-primaryText">
      <Navbar />

      {/* Glow */}
      <div className="pointer-events-none fixed inset-0 overflow-hidden">
        <div className="absolute top-0 left-1/4 w-[500px] h-[500px]
                        rounded-full bg-accent1/8 blur-[120px]" />
      </div>

      <main className="relative z-10 max-w-3xl mx-auto px-6 pt-32 pb-20">
        <motion.div variants={{ show: { transition: { staggerChildren: 0.12 } } }}
          initial="hidden" animate="show">

          {/* Header */}
          <motion.div variants={fadeUp} className="mb-10">
            <p className="text-accent1 text-sm font-medium mb-2 uppercase tracking-widest">Step 1 of 1</p>
            <h1 className="text-4xl font-bold mb-3">Set up your assessment</h1>
            <p className="text-primaryText/50 text-lg">
              Upload your résumé and paste the job description to get started.
            </p>
          </motion.div>

          {/* ── Resume Upload ── */}
          <motion.div variants={fadeUp} className="mb-6">
            <label className="flex items-center gap-2 text-sm font-semibold mb-3
                              text-primaryText/80 uppercase tracking-wider">
              <FileText size={15} className="text-accent1" />
              Résumé (PDF)
            </label>

            <div
              onDragOver={(e) => { e.preventDefault(); setDragging(true) }}
              onDragLeave={() => setDragging(false)}
              onDrop={handleFileDrop}
              onClick={() => document.getElementById('fileInput').click()}
              className={`relative flex flex-col items-center justify-center gap-3 p-10
                         rounded-2xl border-2 border-dashed cursor-pointer
                         transition-all duration-300
                         ${dragging
                           ? 'border-accent1 bg-accent1/10'
                           : resumeData
                             ? 'border-cta/50 bg-cta/8'
                             : 'border-white/10 bg-white/3 hover:border-white/25 hover:bg-white/5'}`}
            >
              <input
                id="fileInput"
                type="file"
                accept=".pdf"
                className="hidden"
                onChange={(e) => handleUpload(e.target.files[0])}
              />

              <AnimatePresence mode="wait">
                {status === 'uploading' ? (
                  <motion.div key="uploading" initial={{ opacity: 0 }} animate={{ opacity: 1 }}>
                    <Loader2 size={32} className="text-accent1 animate-spin" />
                  </motion.div>
                ) : resumeData ? (
                  <motion.div key="done" initial={{ scale: 0.8, opacity: 0 }}
                    animate={{ scale: 1, opacity: 1 }}
                    className="flex flex-col items-center gap-2">
                    <CheckCircle size={32} className="text-cta" />
                    <p className="text-sm font-medium text-primaryText">{resumeFile?.name}</p>
                    <p className="text-xs text-primaryText/40">
                      {resumeData.is_returning_user ? '✦ Returning user — loaded from cache' : '✦ New résumé processed'}
                    </p>
                  </motion.div>
                ) : (
                  <motion.div key="idle" initial={{ opacity: 0 }} animate={{ opacity: 1 }}
                    className="flex flex-col items-center gap-2 text-center">
                    <Upload size={28} className="text-primaryText/30" />
                    <p className="text-sm text-primaryText/50">
                      <span className="text-accent1 font-medium">Click to upload</span> or drag & drop
                    </p>
                    <p className="text-xs text-primaryText/30">PDF files only</p>
                  </motion.div>
                )}
              </AnimatePresence>
            </div>
          </motion.div>

          {/* ── Job Description ── */}
          <motion.div variants={fadeUp} className="mb-8">
            <label className="flex items-center gap-2 text-sm font-semibold mb-3
                              text-primaryText/80 uppercase tracking-wider">
              <Briefcase size={15} className="text-accent2" />
              Job Description
            </label>
            <textarea
              value={jobDescription}
              onChange={(e) => setJobDescription(e.target.value)}
              rows={9}
              placeholder="Paste the full job description here..."
              className="w-full rounded-2xl bg-white/3 border border-white/10 p-5
                         text-primaryText/90 text-sm leading-relaxed resize-none
                         placeholder-primaryText/25 outline-none
                         focus:border-accent1/50 focus:bg-white/5
                         transition-all duration-300"
            />
            <p className="mt-2 text-xs text-primaryText/30 text-right">
              {jobDescription.length} characters {jobDescription.length < 50 && jobDescription.length > 0 ? '— needs more detail' : ''}
            </p>
          </motion.div>

          {/* Error */}
          <AnimatePresence>
            {status === 'error' && (
              <motion.div initial={{ opacity: 0, y: -10 }} animate={{ opacity: 1, y: 0 }}
                exit={{ opacity: 0 }}
                className="flex items-center gap-3 p-4 rounded-xl border border-accent2/30
                           bg-accent2/10 text-accent2 text-sm mb-6">
                <AlertCircle size={16} />
                {errorMsg}
              </motion.div>
            )}
          </AnimatePresence>

          {/* Start Button */}
          <motion.div variants={fadeUp}>
            <motion.button
              whileHover={canStart ? { scale: 1.03, boxShadow: '0 0 32px rgba(0,77,97,0.45)' } : {}}
              whileTap={canStart ? { scale: 0.97 } : {}}
              onClick={handleStart}
              disabled={!canStart}
              className={`w-full flex items-center justify-center gap-3 py-4 rounded-xl
                         font-semibold text-base transition-all duration-300
                         ${canStart
                           ? 'bg-accent1 text-background cursor-pointer'
                           : 'bg-white/5 text-primaryText/25 cursor-not-allowed'}`}
            >
              {status === 'starting'
                ? <><Loader2 size={18} className="animate-spin" /> Starting assessment…</>
                : <><ArrowRight size={18} /> Begin Assessment</>}
            </motion.button>
          </motion.div>

        </motion.div>
      </main>
    </div>
  )
}
