import React, { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { Upload, CheckCircle, AlertCircle, Loader2 } from 'lucide-react'
import Navbar from '../components/Navbar.jsx'
import { uploadResume, startAssessment } from '../services/api.js'

export default function SetupPage() {
  const navigate = useNavigate()
  const [resumeFile, setResumeFile] = useState(null)
  const [jobDescription, setJobDescription] = useState('')
  const [dragging, setDragging] = useState(false)
  const [status, setStatus] = useState('idle')
  const [errorMsg, setErrorMsg] = useState('')
  const [resumeData, setResumeData] = useState(null)

  const handleFileDrop = (e) => {
    e.preventDefault()
    setDragging(false)
    const file = e.dataTransfer?.files[0] || e.target.files[0]
    if (file && file.type === 'application/pdf') {
      handleUpload(file)
    } else {
      setErrorMsg('Please upload a PDF file.')
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
    } catch {
      setErrorMsg('Couldn’t read your resume. Make sure the backend is running and try again.')
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
    } catch {
      setErrorMsg('Something went wrong starting the interview. Try again in a moment.')
      setStatus('error')
    }
  }

  const canStart = resumeData && jobDescription.trim().length > 50 && status === 'idle'

  return (
    <div className="min-h-screen">
      <Navbar />

      <main className="max-w-2xl mx-auto px-5 pt-28 pb-20">
        <div className="mb-8">
          <h1 className="text-2xl font-semibold text-ink mb-2">Set up your session</h1>
          <p className="text-sm text-ink-muted leading-relaxed">
            Upload your resume and paste the job description you want to prepare for.
            We’ll figure out which skills to test and start the interview.
          </p>
        </div>

        <div className="space-y-6">
          {/* Resume */}
          <section className="rounded-xl border border-border bg-surface p-5 shadow-card">
            <label className="block text-sm font-medium text-ink mb-3">Resume (PDF)</label>

            <div
              onDragOver={(e) => { e.preventDefault(); setDragging(true) }}
              onDragLeave={() => setDragging(false)}
              onDrop={handleFileDrop}
              onClick={() => document.getElementById('fileInput').click()}
              className={`flex flex-col items-center justify-center gap-3 p-8 rounded-lg border-2 border-dashed cursor-pointer transition-colors
                ${dragging
                  ? 'border-accent bg-accent-soft'
                  : resumeData
                    ? 'border-success/40 bg-success-soft'
                    : 'border-border-strong hover:border-stone-400 hover:bg-stone-50'}`}
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

              {status === 'uploading' ? (
                <>
                  <Loader2 size={24} className="text-accent animate-spin" />
                  <p className="text-sm text-ink-muted">Reading PDF…</p>
                </>
              ) : resumeData ? (
                <>
                  <CheckCircle size={24} className="text-success" />
                  <div className="text-center">
                    <p className="text-sm font-medium text-ink">{resumeFile?.name}</p>
                    <p className="text-xs text-ink-muted mt-1">
                      {resumeData.is_returning_user ? 'Welcome back — loaded from cache' : 'Uploaded successfully'}
                    </p>
                  </div>
                </>
              ) : (
                <>
                  <Upload size={22} className="text-ink-faint" />
                  <div className="text-center">
                    <p className="text-sm text-ink">
                      Drop your PDF here or <span className="text-accent font-medium">browse</span>
                    </p>
                    <p className="text-xs text-ink-faint mt-1">PDF only</p>
                  </div>
                </>
              )}
            </div>
          </section>

          {/* Job description */}
          <section className="rounded-xl border border-border bg-surface p-5 shadow-card">
            <div className="flex justify-between items-baseline mb-3">
              <label className="text-sm font-medium text-ink">Job description</label>
              <span className="text-xs text-ink-faint">{jobDescription.length} characters</span>
            </div>
            <textarea
              value={jobDescription}
              onChange={(e) => setJobDescription(e.target.value)}
              rows={10}
              placeholder="Paste the full job posting here — requirements, tech stack, responsibilities. The more detail, the better the skill match."
              className="w-full rounded-lg border border-border-strong bg-stone-50/50 px-3.5 py-3 text-sm text-ink leading-relaxed resize-none
                         placeholder:text-ink-faint outline-none focus:border-accent focus:ring-2 focus:ring-accent/10 transition-shadow"
            />
            {jobDescription.length > 0 && jobDescription.length < 50 && (
              <p className="text-xs text-warn mt-2">Add a bit more detail so we can pick the right skills.</p>
            )}
          </section>

          {status === 'error' && (
            <div className="flex items-start gap-2.5 p-4 rounded-lg border border-red-200 bg-red-50 text-red-800 text-sm">
              <AlertCircle size={16} className="shrink-0 mt-0.5" />
              <span>{errorMsg}</span>
            </div>
          )}

          <button
            onClick={handleStart}
            disabled={!canStart}
            className={`w-full py-3 rounded-lg text-sm font-medium transition-colors
              ${canStart
                ? 'bg-ink text-white hover:bg-stone-800'
                : 'bg-stone-200 text-ink-faint cursor-not-allowed'}`}
          >
            {status === 'starting' ? (
              <span className="inline-flex items-center gap-2">
                <Loader2 size={16} className="animate-spin" />
                Starting interview…
              </span>
            ) : (
              'Start interview'
            )}
          </button>
        </div>
      </main>
    </div>
  )
}
