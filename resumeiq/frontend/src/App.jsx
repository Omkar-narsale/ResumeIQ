import React, { useState } from 'react'
import { AuthProvider, AuthContext } from './context/AuthContext'
import { ResumeProvider } from './context/ResumeContext'
import { ChatProvider } from './context/ChatContext'
import { Login } from './pages/Login'
import { Dashboard } from './pages/Dashboard'
import { ResumeUpload } from './pages/ResumeUpload'
import { Analyzer } from './pages/Analyzer'
import { ResumeTemplates } from './pages/ResumeTemplates'
import { JobMatcher } from './pages/JobMatcher'
import { Rewriter } from './pages/Rewriter'
import { CoverLetter } from './pages/CoverLetter'
import { Interview } from './pages/Interview'
import { Learning } from './pages/Learning'
import { KeywordOptimizer } from './pages/KeywordOptimizer'
import { ATSScore } from './pages/ATSScore'
import { SkillGapAnalyzer } from './pages/SkillGapAnalyzer'
import { ResumeComparison } from './pages/ResumeComparison'
import { ResumeVersioning } from './pages/ResumeVersioning'
import { BatchJobMatch } from './pages/BatchJobMatch'
import { Achievements } from './pages/Achievements'
import { CareerToolkit } from './pages/CareerToolkit'
import { CareerCopilot } from './pages/CareerCopilot'
import { Navbar } from './components/Navbar'
import { Sidebar } from './components/Sidebar'

function MainApp() {
  const [currentPage, setCurrentPage] = useState('dashboard')
  const [sidebarOpen, setSidebarOpen] = useState(false)

  const renderPage = () => {
    switch (currentPage) {
      case 'dashboard': return <Dashboard onNavigate={setCurrentPage} />
      case 'resume': return <ResumeUpload />
      case 'templates': return <ResumeTemplates />
      case 'analyze': return <Analyzer />
      case 'matcher': return <JobMatcher />
      case 'batch-match': return <BatchJobMatch />
      case 'rewriter': return <Rewriter />
      case 'cover-letter': return <CoverLetter />
      case 'interview': return <Interview />
      case 'learning': return <Learning />
      case 'keyword-optimizer': return <KeywordOptimizer />
      case 'ats-score': return <ATSScore />
      case 'skill-gap': return <SkillGapAnalyzer />
      case 'compare': return <ResumeComparison />
      case 'versioning': return <ResumeVersioning />
      case 'achievements': return <Achievements />
      case 'linkedin-optimizer': return <CareerToolkit initialTab="linkedin" />
      case 'star-responses': return <CareerToolkit initialTab="star" />
      case 'email-templates': return <CareerToolkit initialTab="email" />
      case 'portfolio-showcase': return <CareerToolkit initialTab="portfolio" />
      case 'ai-career-copilot': return <CareerCopilot />
      default: return <Dashboard onNavigate={setCurrentPage} />
    }
  }

  return (
    <div className="flex h-screen bg-gray-900">
      <Sidebar
        isOpen={sidebarOpen}
        currentPage={currentPage}
        onNavigate={setCurrentPage}
        onClose={() => setSidebarOpen(false)}
      />

      <div className="flex-1 flex flex-col overflow-hidden">
        <Navbar onMenuClick={() => setSidebarOpen(!sidebarOpen)} />

        <main className="flex-1 overflow-auto p-6">
          <div className="max-w-7xl mx-auto">
            {renderPage()}
          </div>
        </main>
      </div>
    </div>
  )
}

function App() {
  return (
    <AuthProvider>
      <ResumeProvider>
        <ChatProvider>
          <AuthContext.Consumer>
            {({ token, loading }) => {
              if (loading) {
                return (
                  <div className="min-h-screen bg-gradient-to-br from-gray-900 via-gray-800 to-black flex items-center justify-center">
                    <div className="text-center">
                      <div className="w-12 h-12 border-4 border-blue-500 border-t-transparent rounded-full animate-spin mx-auto mb-4" />
                      <p className="text-gray-400">Loading...</p>
                    </div>
                  </div>
                )
              }

              if (!token) {
                return <Login />
              }

              return <MainApp />
            }}
          </AuthContext.Consumer>
        </ChatProvider>
      </ResumeProvider>
    </AuthProvider>
  )
}

export default App
