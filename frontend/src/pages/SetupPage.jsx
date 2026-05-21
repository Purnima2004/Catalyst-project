import React, { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { motion, AnimatePresence } from 'framer-motion'
import { Upload, FileText, Briefcase, ArrowRight, CheckCircle, AlertCircle, Loader2, Info, ChevronRight } from 'lucide-react'
import Navbar from '../components/Navbar.jsx'
import { uploadResume, startAssessment } from '../services/api.js'

const fadeUp = {
  hidden: { opacity: 0, y: 15 },
  show: { opacity: 1, y: 0, transition: { duration: 0.5, ease: [0.19, 1, 0.22, 1] } },
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
    if (file && file.type === 'application/pdf') {
      handleUpload(file)
    } else {
      setErrorMsg('Invalid file type. Only PDF resumes are supported.')
      setStatus('error')
    }
  }

  const handleUpload = async (file) => {
    setResumeFile(file)
    setStatus('uploading')
    setErrorMsg('')
    try {
      const data = await uploadResume(file)
      setResumeData(data)
      setStatus('idle')
    } catch (err) {
      setErrorMsg('Failed to process resume. Please verify that the backend engine is active.')
      setStatus('error')
    }
  }

  const handleStart = async () => {
    if (!resumeData || !jobDescription.trim()) return
    setStatus('starting')
    setErrorMsg('')
    try {
      const result = await startAssessment({
        job_description: jobDescription,
        resume_hash: resumeData.resume_hash,
        resume_text: resumeData.resume_text,
        is_returning_user: resumeData.is_returning_user,
      })
      sessionStorage.setItem('catalyst_thread_id', result.thread_id)
      sessionStorage.setItem('catalyst_state', JSON.stringify(result))
      navigate('/assessment')
    } catch (err) {
      setErrorMsg('Failed to launch assessment workspace. Please try again.')
      setStatus('error')
    }
  }

  const canStart = resumeData && jobDescription.trim().length > 50 && status === 'idle'

  return (
    <div className="min-h-screen text-primaryText selection:bg-accent1/35 selection:text-white">
      <Navbar />

      <main className="relative z-10 max-w-6xl mx-auto px-6 pt-32 pb-20">
        <div className="grid grid-cols-1 lg:grid-cols-12 gap-8 items-start">
          
          {/* Left Column: Guidelines / Overview */}
          <motion.div
            initial={{ opacity: 0, y: 15 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5, ease: [0.19, 1, 0.22, 1] }}
            className="lg:col-span-4 lg:sticky lg:top-32 space-y-6"
          >
            <div>
              <span className="text-[10px] font-mono tracking-widest text-accent1 uppercase">Setup Panel</span>
              <h1 className="text-3xl font-bold text-white mt-1 mb-3">Configure Assessment</h1>
              <p className="text-text-muted text-sm font-light leading-relaxed">
                Provide your background credentials and the target job description to configure your custom assessment session.
              </p>
            </div>

            {/* Steps Visual Check */}
            <div className="rounded-xl border border-white/5 bg-panel p-5 space-y-4 relative">
              <div className="absolute inset-[1px] rounded-[11px] border border-white/[0.01] pointer-events-none" />
              
              <h3 className="text-xs font-semibold text-white tracking-wide uppercase">Workflow Checklist</h3>
              
              <div className="space-y-3 text-xs">
                {/* Step 1 */}
                <div className="flex items-center gap-3">
                  <div className={`w-5 h-5 rounded-full flex items-center justify-center border font-mono text-[9px] font-bold transition-all duration-300
                    ${resumeData 
                      ? 'bg-cta/10 border-cta text-cta' 
                      : 'bg-white/5 border-white/10 text-text-muted'}`}>
                    {resumeData ? <CheckCircle size={10} /> : '1'}
                  </div>
                  <div>
                    <p className={`font-medium ${resumeData ? 'text-white' : 'text-text-muted'}`}>Upload credentials</p>
                    <p className="text-[10px] text-text-muted/65 mt-0.5">Resume PDF</p>
                  </div>
                </div>

                {/* Step 2 */}
                <div className="flex items-center gap-3">
                  <div className={`w-5 h-5 rounded-full flex items-center justify-center border font-mono text-[9px] font-bold transition-all duration-300
                    ${jobDescription.trim().length > 50 
                      ? 'bg-cta/10 border-cta text-cta' 
                      : 'bg-white/5 border-white/10 text-text-muted'}`}>
                    {jobDescription.trim().length > 50 ? <CheckCircle size={10} /> : '2'}
                  </div>
                  <div>
                    <p className={`font-medium ${jobDescription.trim().length > 50 ? 'text-white' : 'text-text-muted'}`}>Define target role</p>
                    <p className="text-[10px] text-text-muted/65 mt-0.5">Job specification text</p>
                  </div>
                </div>
              </div>
            </div>

            {/* Info Notice */}
            <div className="flex gap-2.5 p-4 rounded-xl bg-white/[0.01] border border-white/5 text-xs text-text-muted leading-relaxed font-light">
              <Info size={14} className="text-accent2 shrink-0 mt-0.5" />
              <p>
                Credentials are parsed deterministically. Your skill graphs are compiled without LLM hallucinations.
              </p>
            </div>
          </motion.div>

          {/* Right Column: Uploader & Fields */}
          <motion.div
            initial={{ opacity: 0, y: 15 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5, ease: [0.19, 1, 0.22, 1], delay: 0.1 }}
            className="lg:col-span-8 space-y-6"
          >
            {/* ── Resume Upload Section ── */}
            <div className="rounded-xl border border-white/5 bg-panel p-6 space-y-4 relative">
              <div className="absolute inset-[1px] rounded-[11px] border border-white/[0.01] pointer-events-none" />

              <label className="flex items-center gap-2 text-xs font-semibold text-white tracking-wider uppercase">
                <FileText size={14} className="text-accent1" />
                Professional résumé (PDF format)
              </label>

              <div
                onDragOver={(e) => { e.preventDefault(); setDragging(true) }}
                onDragLeave={() => setDragging(false)}
                onDrop={handleFileDrop}
                onClick={() => document.getElementById('fileInput').click()}
                className={`relative flex flex-col items-center justify-center gap-4 p-10
                           rounded-xl border-2 border-dashed cursor-pointer transition-all duration-300
                           ${dragging
                             ? 'border-accent1 bg-accent1/5'
                             : resumeData
                               ? 'border-cta/30 bg-cta/[0.02] hover:border-cta/50'
                               : 'border-white/10 bg-white/[0.01] hover:border-white/20 hover:bg-white/[0.02]'}`}
              >
                <input
                  id="fileInput"
                  type="file"
                  accept=".pdf"
                  className="hidden"
                  onChange={(e) => {
                    if (e.target.files[0]) handleUpload(e.target.files[0])
                  }}
                />

                <AnimatePresence mode="wait">
                  {status === 'uploading' ? (
                    <motion.div 
                      key="uploading" 
                      initial={{ opacity: 0 }} 
                      animate={{ opacity: 1 }}
                      className="flex flex-col items-center gap-2 text-center"
                    >
                      <Loader2 size={26} className="text-accent1 animate-spin" />
                      <p className="text-xs text-white font-medium">Extracting credential blueprint...</p>
                    </motion.div>
                  ) : resumeData ? (
                    <motion.div 
                      key="done" 
                      initial={{ scale: 0.96, opacity: 0 }}
                      animate={{ scale: 1, opacity: 1 }}
                      className="flex flex-col items-center gap-2.5 text-center"
                    >
                      <div className="w-9 h-9 rounded-full bg-cta/10 border border-cta/30 flex items-center justify-center">
                        <CheckCircle size={18} className="text-cta" />
                      </div>
                      <div>
                        <p className="text-xs font-semibold text-white tracking-wide">{resumeFile?.name}</p>
                        <p className="text-[10px] text-text-muted mt-1 font-mono uppercase tracking-wider">
                          {resumeData.is_returning_user ? '✦ Returning Candidate — Loaded Cache' : '✦ Parse Blueprint Success'}
                        </p>
                      </div>
                    </motion.div>
                  ) : (
                    <motion.div 
                      key="idle" 
                      initial={{ opacity: 0 }} 
                      animate={{ opacity: 1 }}
                      className="flex flex-col items-center gap-2.5 text-center"
                    >
                      <div className="w-9 h-9 rounded-lg bg-white/5 border border-white/10 flex items-center justify-center">
                        <Upload size={16} className="text-text-muted" />
                      </div>
                      <div>
                        <p className="text-xs font-medium text-white">
                          <span className="text-accent1 hover:underline">Choose file</span> or drag & drop here
                        </p>
                        <p className="text-[10px] text-text-muted mt-1 font-light">PDF documents only (max 10MB)</p>
                      </div>
                    </motion.div>
                  )}
                </AnimatePresence>
              </div>
            </div>

            {/* ── Job Description Section ── */}
            <div className="rounded-xl border border-white/5 bg-panel p-6 space-y-4 relative">
              <div className="absolute inset-[1px] rounded-[11px] border border-white/[0.01] pointer-events-none" />

              <div className="flex justify-between items-center">
                <label className="flex items-center gap-2 text-xs font-semibold text-white tracking-wider uppercase">
                  <Briefcase size={14} className="text-accent2" />
                  Target job specification
                </label>
                <span className="text-[9px] font-mono text-text-muted">
                  {jobDescription.length} chars
                </span>
              </div>

              <div className="relative border border-white/10 rounded-lg overflow-hidden bg-black/20 focus-within:border-accent1/40 transition-colors duration-300">
                <textarea
                  value={jobDescription}
                  onChange={(e) => setJobDescription(e.target.value)}
                  rows={8}
                  placeholder="Paste the full, detailed job description here..."
                  className="w-full bg-transparent p-4 text-white text-xs leading-relaxed resize-none
                             placeholder-text-muted/40 outline-none font-light"
                />
                
                {jobDescription.length < 50 && jobDescription.length > 0 && (
                  <div className="absolute bottom-3 left-4 flex items-center gap-1.5 text-[9px] text-accent2">
                    <Info size={10} />
                    <span>Please provide a more comprehensive description to match skill matrices accurately.</span>
                  </div>
                )}
              </div>
            </div>

            {/* Error Message */}
            <AnimatePresence>
              {status === 'error' && (
                <motion.div 
                  initial={{ opacity: 0, y: -8 }} 
                  animate={{ opacity: 1, y: 0 }}
                  exit={{ opacity: 0 }}
                  className="flex items-center gap-2.5 p-4 rounded-lg border border-accent2/20 bg-accent2/5 text-accent2 text-xs"
                >
                  <AlertCircle size={14} className="shrink-0" />
                  <span>{errorMsg}</span>
                </motion.div>
              )}
            </AnimatePresence>

            {/* Begin Assessment Button */}
            <div>
              <motion.button
                whileHover={canStart ? { y: -1 } : {}}
                whileTap={canStart ? { y: 0 } : {}}
                onClick={handleStart}
                disabled={!canStart}
                className={`w-full flex items-center justify-center gap-2 py-3.5 rounded
                           font-semibold text-xs tracking-widest uppercase transition-all duration-300 border
                           ${canStart
                             ? 'bg-white hover:bg-slate-100 text-black border-white hover:border-slate-100 shadow-sm cursor-pointer'
                             : 'bg-white/5 text-text-muted/30 border-white/5 cursor-not-allowed'}`}
              >
                {status === 'starting' ? (
                  <>
                    <Loader2 size={13} className="animate-spin text-black" />
                    Initializing assessment workspace...
                  </>
                ) : (
                  <>
                    Begin Assessment workspace
                    <ArrowRight size={13} />
                  </>
                )}
              </motion.button>
            </div>

          </motion.div>

        </div>
      </main>
    </div>
  )
}
