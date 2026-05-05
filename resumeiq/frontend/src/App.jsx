import React, { useState } from 'react'
import { AuthProvider, AuthContext } from './context/AuthContext'
import { ResumeProvider } from './context/ResumeContext'
import { Login } from './pages/Login'
import { Dashboard } from './pages/Dashboard'
import { ResumeUpload } from './pages/ResumeUpload'
import { Analyzer } from './pages/Analyzer'
import { JobMatcher } from './pages/JobMatcher'
import { Rewriter } from './pages/Rewriter'
import { CoverLetter } from './pages/CoverLetter'
import { Interview } from './pages/Interview'
import { Learning } from './pages/Learning'
import { Navbar } from './components/Navbar'
import { Sidebar } from './components/Sidebar'

function MainApp() {
  const [currentPage, setCurrentPage] = useState('dashboard')
  const [sidebarOpen, setSidebarOpen] = useState(false)

  const renderPage = () => {
    switch (currentPage) {
      case 'dashboard': return <Dashboard onNavigate={setCurrentPage} />
      case 'resume': return <ResumeUpload />
      case 'analyze': return <Analyzer />
      case 'matcher': return <JobMatcher />
      case 'rewriter': return <Rewriter />
      case 'cover-letter': return <CoverLetter />
      case 'interview': return <Interview />
      case 'learning': return <Learning />
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
      </ResumeProvider>
    </AuthProvider>
  )
}

export default App
