import React from 'react'
import { BrowserRouter, Routes, Route } from 'react-router-dom'
import LandingPage from './pages/LandingPage.jsx'
import SetupPage from './pages/SetupPage.jsx'
import AssessmentPage from './pages/AssessmentPage.jsx'
import ResultsPage from './pages/ResultsPage.jsx'

function App() {
  return (
    <BrowserRouter>
      <div className="min-h-screen bg-background text-primaryText font-sans selection:bg-accent1 selection:text-white">
        <Routes>
          <Route path="/" element={<LandingPage />} />
          <Route path="/setup" element={<SetupPage />} />
          <Route path="/assessment" element={<AssessmentPage />} />
          <Route path="/results" element={<ResultsPage />} />
        </Routes>
      </div>
    </BrowserRouter>
  )
}

export default App
