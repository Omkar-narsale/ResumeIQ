import React, { useState, useContext, useEffect } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import { AuthContext } from '../context/AuthContext'
import { Card, CardTitle, CardContent } from '../components/Card'
import { pageVariants, containerVariants, itemVariants } from '../components/animations'
import { ToolkitCard, ToolkitSection, ToolkitFeatureBox } from '../components/ToolkitCard'

const API_BASE = 'http://localhost:8000/api'

const tabs = [
  { id: 'linkedin', label: 'LinkedIn Optimizer', icon: '💼' },
  { id: 'star', label: 'STAR Responses', icon: '⭐' },
  { id: 'email', label: 'Email Templates', icon: '📧' },
  { id: 'portfolio', label: 'Portfolio Showcase', icon: '🎁' }
]

export const CareerToolkit = ({ initialTab = 'linkedin' }) => {
  const [activeTab, setActiveTab] = useState(initialTab)
  const [key, setKey] = useState(0)

  useEffect(() => {
    setKey(prev => prev + 1)
  }, [activeTab])

  const renderContent = () => {
    switch (activeTab) {
      case 'linkedin':
        return <LinkedInOptimizer />
      case 'star':
        return <StarResponses />
      case 'email':
        return <EmailTemplates />
      case 'portfolio':
        return <PortfolioShowcase />
      default:
        return <LinkedInOptimizer />
    }
  }

  return (
    <motion.div
      className="space-y-6"
      variants={pageVariants}
      initial="hidden"
      animate="visible"
    >
      <Card>
        <CardTitle>🚀 Career Toolkit</CardTitle>
        <CardContent className="text-sm text-gray-400">
          AI-powered tools to accelerate your career growth and professional development
        </CardContent>
      </Card>

      <motion.div
        className="flex gap-3 p-4 bg-gray-800 bg-opacity-50 rounded-lg overflow-x-auto"
        variants={containerVariants}
      >
        {tabs.map((tab) => (
          <motion.button
            key={tab.id}
            onClick={() => setActiveTab(tab.id)}
            className={`px-4 py-2 rounded-lg whitespace-nowrap transition-all flex items-center gap-2 text-sm font-medium ${
              activeTab === tab.id
                ? 'bg-blue-500 text-white shadow-lg shadow-blue-500/50'
                : 'bg-gray-700 text-gray-300 hover:bg-gray-600'
            }`}
            whileHover={{ scale: 1.05 }}
            whileTap={{ scale: 0.98 }}
          >
            <span>{tab.icon}</span>
            {tab.label}
          </motion.button>
        ))}
      </motion.div>

      <AnimatePresence mode="wait">
        <motion.div
          key={`${activeTab}-${key}`}
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          exit={{ opacity: 0 }}
          transition={{ duration: 0.2 }}
        >
          {renderContent()}
        </motion.div>
      </AnimatePresence>
    </motion.div>
  )
}

// LinkedIn Optimizer
const LinkedInOptimizer = () => {
  const { token } = useContext(AuthContext)
  const [formData, setFormData] = useState({
    headline: '',
    about_section: '',
    skills: '',
    target_role: ''
  })
  const [result, setResult] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')

  const handleSubmit = async (e) => {
    e.preventDefault()
    setLoading(true)
    setError('')

    try {
      const skillsArray = formData.skills
        .split(',')
        .map(s => s.trim())
        .filter(s => s)

      const response = await fetch(`${API_BASE}/linkedin-optimizer`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify({
          headline: formData.headline,
          about_section: formData.about_section,
          skills: skillsArray,
          target_role: formData.target_role
        })
      })

      if (!response.ok) throw new Error('Failed to optimize')
      const data = await response.json()
      setResult(data)
    } catch (err) {
      setError(err.message)
    } finally {
      setLoading(false)
    }
  }

  const copyToClipboard = (text) => {
    navigator.clipboard.writeText(text)
  }

  return (
    <ToolkitSection
      title="💼 LinkedIn Optimizer"
      description="Enhance your LinkedIn profile to attract recruiters and stand out"
    >
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Input Form */}
        <motion.div
          className="bg-gray-800 bg-opacity-50 p-6 rounded-lg border border-gray-700"
          initial={{ opacity: 0, x: -20 }}
          animate={{ opacity: 1, x: 0 }}
          transition={{ duration: 0.3 }}
        >
          <h3 className="text-lg font-semibold text-white mb-4">Profile Information</h3>
          <form onSubmit={handleSubmit} className="space-y-4">
            <div>
              <label className="block text-sm font-medium text-gray-300 mb-2">Current Headline</label>
              <input
                type="text"
                value={formData.headline}
                onChange={(e) => setFormData({...formData, headline: e.target.value})}
                placeholder="e.g., Senior Software Engineer"
                className="w-full px-4 py-2 bg-gray-700 border border-gray-600 rounded text-white placeholder-gray-400 focus:outline-none focus:border-blue-500"
                required
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-300 mb-2">About Section</label>
              <textarea
                value={formData.about_section}
                onChange={(e) => setFormData({...formData, about_section: e.target.value})}
                placeholder="Your current About section..."
                rows="4"
                className="w-full px-4 py-2 bg-gray-700 border border-gray-600 rounded text-white placeholder-gray-400 focus:outline-none focus:border-blue-500"
                required
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-300 mb-2">Skills (comma-separated)</label>
              <input
                type="text"
                value={formData.skills}
                onChange={(e) => setFormData({...formData, skills: e.target.value})}
                placeholder="Python, JavaScript, Leadership, Project Management"
                className="w-full px-4 py-2 bg-gray-700 border border-gray-600 rounded text-white placeholder-gray-400 focus:outline-none focus:border-blue-500"
                required
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-300 mb-2">Target Role</label>
              <input
                type="text"
                value={formData.target_role}
                onChange={(e) => setFormData({...formData, target_role: e.target.value})}
                placeholder="e.g., Engineering Manager"
                className="w-full px-4 py-2 bg-gray-700 border border-gray-600 rounded text-white placeholder-gray-400 focus:outline-none focus:border-blue-500"
                required
              />
            </div>

            <button
              type="submit"
              disabled={loading}
              className="w-full px-4 py-2 bg-blue-500 hover:bg-blue-600 text-white rounded font-medium transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
            >
              {loading ? 'Optimizing...' : 'Optimize Profile'}
            </button>

            {error && <p className="text-red-400 text-sm">{error}</p>}
          </form>
        </motion.div>

        {/* Results */}
        {result && (
          <motion.div
            className="space-y-4"
            initial={{ opacity: 0, x: 20 }}
            animate={{ opacity: 1, x: 0 }}
          >
            <div className="bg-gradient-to-r from-blue-500 to-purple-500 p-1 rounded-lg">
              <div className="bg-gray-900 p-4 rounded">
                <div className="flex justify-between items-start mb-3">
                  <h3 className="text-white font-semibold">Profile Strength Score</h3>
                  <span className="text-2xl font-bold text-blue-400">{result.profile_strength_score.toFixed(0)}/100</span>
                </div>
                <div className="w-full bg-gray-700 rounded-full h-2">
                  <div
                    className="bg-gradient-to-r from-blue-500 to-purple-500 h-2 rounded-full"
                    style={{ width: `${result.profile_strength_score}%` }}
                  />
                </div>
              </div>
            </div>

            <div className="bg-gray-800 bg-opacity-50 p-4 rounded-lg border border-gray-700">
              <h4 className="text-white font-semibold mb-2">✨ Optimized Headline</h4>
              <p className="text-gray-300 mb-3">{result.optimized_headline}</p>
              <button
                onClick={() => copyToClipboard(result.optimized_headline)}
                className="text-blue-400 hover:text-blue-300 text-sm font-medium"
              >
                📋 Copy
              </button>
            </div>

            <div className="bg-gray-800 bg-opacity-50 p-4 rounded-lg border border-gray-700">
              <h4 className="text-white font-semibold mb-2">📝 Optimized About</h4>
              <p className="text-gray-300 mb-3 text-sm leading-relaxed">{result.optimized_about}</p>
              <button
                onClick={() => copyToClipboard(result.optimized_about)}
                className="text-blue-400 hover:text-blue-300 text-sm font-medium"
              >
                📋 Copy
              </button>
            </div>

            <div className="bg-gray-800 bg-opacity-50 p-4 rounded-lg border border-gray-700">
              <h4 className="text-white font-semibold mb-3">🔑 Suggested Keywords</h4>
              <div className="flex flex-wrap gap-2">
                {result.suggested_keywords.map((keyword, i) => (
                  <motion.span
                    key={i}
                    className="px-3 py-1 bg-blue-500 bg-opacity-20 text-blue-300 text-xs rounded-full border border-blue-500 border-opacity-30 cursor-pointer hover:bg-opacity-30"
                    onClick={() => copyToClipboard(keyword)}
                    whileHover={{ scale: 1.1 }}
                  >
                    {keyword}
                  </motion.span>
                ))}
              </div>
            </div>

            {result.missing_skills.length > 0 && (
              <div className="bg-gray-800 bg-opacity-50 p-4 rounded-lg border border-yellow-500 border-opacity-30">
                <h4 className="text-yellow-400 font-semibold mb-2">⚠️ Skills to Consider Adding</h4>
                <ul className="space-y-1">
                  {result.missing_skills.map((skill, i) => (
                    <li key={i} className="text-sm text-gray-300">• {skill}</li>
                  ))}
                </ul>
              </div>
            )}
          </motion.div>
        )}
      </div>

      {!result && (
        <motion.div
          className="grid grid-cols-1 md:grid-cols-3 gap-4"
          variants={containerVariants}
        >
          <ToolkitCard
            icon="👤"
            title="Headline Optimization"
            description="Create a compelling headline that matches your career goals"
            tags={['Professional', 'Keywords', 'Recruiter-friendly']}
          />
          <ToolkitCard
            icon="📝"
            title="About Section"
            description="Write an engaging about section with impact statements"
            tags={['Story-driven', 'Professional', 'Conversion-focused']}
          />
          <ToolkitCard
            icon="🔑"
            title="Keyword Strategy"
            description="Optimize your profile with recruiter-friendly keywords"
            tags={['SEO', 'Keywords', 'Visibility']}
          />
        </motion.div>
      )}
    </ToolkitSection>
  )
}

// STAR Responses - FULLY ENHANCED
const StarResponses = () => {
  const { token } = useContext(AuthContext)
  const [formData, setFormData] = useState({
    question: '',
    difficulty: 'medium',
    domain: ''
  })
  const [result, setResult] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')
  const [expandedSection, setExpandedSection] = useState(null)
  const [copied, setCopied] = useState(null)

  const commonQuestions = [
    'Tell me about a challenge you overcame',
    'Describe a time you showed leadership',
    'How do you handle working in a team?',
    'Give an example of improving a process',
    'Tell me about a failed project and what you learned',
    'Describe how you resolved a conflict',
    'Tell me about your biggest achievement',
    'How do you handle pressure and tight deadlines?'
  ]

  const starSections = [
    { label: '🎬 Situation', key: 'situation', color: 'from-blue-500 to-blue-600', desc: 'Context & Background' },
    { label: '📋 Task', key: 'task', color: 'from-purple-500 to-purple-600', desc: 'Challenge & Responsibility' },
    { label: '⚡ Action', key: 'action', color: 'from-orange-500 to-orange-600', desc: 'Your Specific Steps' },
    { label: '🎯 Result', key: 'result', color: 'from-green-500 to-green-600', desc: 'Outcome & Impact' }
  ]

  const handleSubmit = async (e) => {
    e.preventDefault()
    setLoading(true)
    setError('')
    setResult(null)
    setExpandedSection(null)

    try {
      const response = await fetch(`${API_BASE}/star-response`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify({
          question: formData.question,
          difficulty: formData.difficulty,
          domain: formData.domain || null
        })
      })

      if (!response.ok) {
        const errorData = await response.json().catch(() => ({ detail: 'Failed to generate' }))
        throw new Error(errorData.detail || 'Failed to generate response')
      }
      const data = await response.json()
      setResult(data)
      setExpandedSection('situation')
    } catch (err) {
      setError(err.message)
    } finally {
      setLoading(false)
    }
  }

  const handleRegenerate = () => {
    setResult(null)
    setExpandedSection(null)
    handleSubmit({ preventDefault: () => {} })
  }

  const copyToClipboard = (text, section) => {
    navigator.clipboard.writeText(text)
    setCopied(section)
    setTimeout(() => setCopied(null), 2000)
  }

  const getDifficultyColor = (difficulty) => {
    const colors = {
      easy: 'bg-green-500 bg-opacity-20 text-green-300 border-green-500',
      medium: 'bg-yellow-500 bg-opacity-20 text-yellow-300 border-yellow-500',
      advanced: 'bg-red-500 bg-opacity-20 text-red-300 border-red-500'
    }
    return colors[difficulty] || colors.medium
  }

  return (
    <ToolkitSection
      title="⭐ STAR Responses"
      description="Master behavioral interviews with structured STAR methodology responses"
    >
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Input Form */}
        <motion.div
          className="bg-gray-800 bg-opacity-50 p-6 rounded-lg border border-gray-700"
          initial={{ opacity: 0, x: -20 }}
          animate={{ opacity: 1, x: 0 }}
          transition={{ duration: 0.3 }}
        >
          <h3 className="text-lg font-semibold text-white mb-4">Generate STAR Response</h3>
          <form onSubmit={handleSubmit} className="space-y-4">
            <div>
              <label className="block text-sm font-medium text-gray-300 mb-2">Behavioral Question *</label>
              <textarea
                value={formData.question}
                onChange={(e) => setFormData({...formData, question: e.target.value})}
                placeholder="Enter or select a behavioral interview question..."
                rows="3"
                className="w-full px-4 py-2 bg-gray-700 border border-gray-600 rounded text-white placeholder-gray-400 focus:outline-none focus:border-blue-500 focus:ring-1 focus:ring-blue-500/50"
                required
              />
              <div className="mt-3 space-y-2">
                <p className="text-xs text-gray-400 font-semibold">Quick Select:</p>
                <div className="space-y-1 max-h-32 overflow-y-auto">
                  {commonQuestions.map((q, i) => (
                    <motion.button
                      key={i}
                      type="button"
                      onClick={() => setFormData({...formData, question: q})}
                      className="text-xs text-blue-400 hover:text-blue-300 hover:bg-blue-500/10 block text-left p-2 rounded w-full transition-colors"
                      whileHover={{ x: 4 }}
                    >
                      → {q}
                    </motion.button>
                  ))}
                </div>
              </div>
            </div>

            <div className="grid grid-cols-2 gap-3">
              <div>
                <label className="block text-sm font-medium text-gray-300 mb-2">Difficulty</label>
                <select
                  value={formData.difficulty}
                  onChange={(e) => setFormData({...formData, difficulty: e.target.value})}
                  className="w-full px-3 py-2 bg-gray-700 border border-gray-600 rounded text-white text-sm focus:outline-none focus:border-blue-500"
                >
                  <option value="easy">Easy</option>
                  <option value="medium">Medium</option>
                  <option value="advanced">Advanced</option>
                </select>
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-300 mb-2">Your Domain</label>
                <input
                  type="text"
                  value={formData.domain}
                  onChange={(e) => setFormData({...formData, domain: e.target.value})}
                  placeholder="Engineering, Product, etc"
                  className="w-full px-3 py-2 bg-gray-700 border border-gray-600 rounded text-white text-sm placeholder-gray-500 focus:outline-none focus:border-blue-500"
                />
              </div>
            </div>

            <div className="flex gap-2 pt-2">
              <motion.button
                type="submit"
                disabled={loading || !formData.question}
                whileHover={{ scale: 1.02 }}
                whileTap={{ scale: 0.98 }}
                className="flex-1 px-4 py-2 bg-gradient-to-r from-blue-500 to-blue-600 hover:from-blue-600 hover:to-blue-700 text-white rounded font-medium transition-all disabled:opacity-50 disabled:cursor-not-allowed"
              >
                {loading ? (
                  <span className="flex items-center justify-center gap-2">
                    <div className="w-4 h-4 border-2 border-blue-200 border-t-white rounded-full animate-spin" />
                    Generating...
                  </span>
                ) : (
                  'Generate Response'
                )}
              </motion.button>
              {result && (
                <motion.button
                  type="button"
                  onClick={handleRegenerate}
                  className="px-4 py-2 bg-gray-700 hover:bg-gray-600 text-white rounded font-medium transition-colors"
                  whileHover={{ scale: 1.02 }}
                  whileTap={{ scale: 0.98 }}
                >
                  🔄 Regenerate
                </motion.button>
              )}
            </div>

            {error && (
              <motion.div
                className="p-3 bg-red-500/20 border border-red-500/50 rounded text-red-300 text-sm"
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
              >
                {error}
              </motion.div>
            )}
          </form>
        </motion.div>

        {/* Results - Expandable STAR Cards */}
        <AnimatePresence mode="wait">
          {result ? (
            <motion.div
              className="space-y-3"
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: -20 }}
            >
              {/* Difficulty Badge */}
              <motion.div
                className="flex gap-3 items-center p-3 bg-gray-800/50 rounded-lg border border-gray-700"
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
              >
                <span className="text-2xl">⭐</span>
                <div>
                  <p className="text-xs text-gray-400">Interview Level</p>
                  <span className={`inline-block px-3 py-1 text-xs font-semibold rounded-full border ${getDifficultyColor(result.difficulty_tag.toLowerCase())}`}>
                    {result.difficulty_tag}
                  </span>
                </div>
              </motion.div>

              {/* STAR Sections */}
              {starSections.map((section, idx) => (
                <motion.div
                  key={section.key}
                  initial={{ opacity: 0, y: 10 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ delay: idx * 0.1 }}
                >
                  <motion.button
                    onClick={() => setExpandedSection(expandedSection === section.key ? null : section.key)}
                    className={`w-full text-left p-4 rounded-lg border-2 transition-all ${
                      expandedSection === section.key
                        ? `bg-gradient-to-r ${section.color} bg-opacity-20 border-${section.color.split('-')[1]}-500`
                        : 'bg-gray-800/30 border-gray-700 hover:border-gray-600'
                    }`}
                    whileHover={{ scale: 1.01 }}
                  >
                    <div className="flex justify-between items-start">
                      <div>
                        <h4 className="font-semibold text-white mb-1">{section.label}</h4>
                        <p className="text-xs text-gray-400">{section.desc}</p>
                      </div>
                      <motion.span
                        animate={{ rotate: expandedSection === section.key ? 180 : 0 }}
                        className="text-lg"
                      >
                        ▼
                      </motion.span>
                    </div>
                  </motion.button>

                  <AnimatePresence>
                    {expandedSection === section.key && (
                      <motion.div
                        className="mt-2 p-4 bg-gray-800/50 rounded-lg border border-gray-700"
                        initial={{ opacity: 0, height: 0 }}
                        animate={{ opacity: 1, height: 'auto' }}
                        exit={{ opacity: 0, height: 0 }}
                      >
                        <p className="text-gray-300 text-sm leading-relaxed mb-3 whitespace-pre-wrap">
                          {result[section.key]}
                        </p>
                        <motion.button
                          onClick={() => copyToClipboard(result[section.key], section.key)}
                          className={`text-sm font-medium px-3 py-1 rounded transition-all ${
                            copied === section.key
                              ? 'bg-green-500/20 text-green-400'
                              : 'bg-blue-500/20 text-blue-400 hover:bg-blue-500/30'
                          }`}
                          whileHover={{ scale: 1.05 }}
                        >
                          {copied === section.key ? '✓ Copied!' : '📋 Copy Section'}
                        </motion.button>
                      </motion.div>
                    )}
                  </AnimatePresence>
                </motion.div>
              ))}

              {/* Full Answer */}
              <motion.div
                className="bg-gradient-to-r from-blue-500/20 to-purple-500/20 border border-blue-500/30 rounded-lg p-4 mt-4"
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                transition={{ delay: 0.4 }}
              >
                <h4 className="text-white font-semibold mb-2 flex items-center gap-2">
                  <span>📢</span> Complete Interview Answer
                </h4>
                <p className="text-gray-300 text-sm leading-relaxed mb-3 max-h-48 overflow-y-auto whitespace-pre-wrap">
                  {result.full_answer}
                </p>
                <motion.button
                  onClick={() => copyToClipboard(result.full_answer, 'full')}
                  className={`text-sm font-medium px-4 py-2 rounded transition-all w-full ${
                    copied === 'full'
                      ? 'bg-green-500/20 text-green-400'
                      : 'bg-blue-500/30 text-blue-300 hover:bg-blue-500/50'
                  }`}
                  whileHover={{ scale: 1.02 }}
                >
                  {copied === 'full' ? '✓ Copied to Clipboard!' : '📋 Copy Full Answer'}
                </motion.button>
              </motion.div>
            </motion.div>
          ) : (
            !result && !loading && (
              <motion.div
                className="flex items-center justify-center h-96 text-center text-gray-400"
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
              >
                <div>
                  <p className="text-4xl mb-2">⭐</p>
                  <p>Select a question and generate your STAR response</p>
                </div>
              </motion.div>
            )
          )}
        </AnimatePresence>
      </div>
    </ToolkitSection>
  )
}

// Email Templates - FULLY ENHANCED
const EmailTemplates = () => {
  const { token } = useContext(AuthContext)
  const [formData, setFormData] = useState({
    template_type: 'job_outreach',
    user_name: '',
    company_name: '',
    role: '',
    additional_context: ''
  })
  const [result, setResult] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')
  const [copied, setCopied] = useState(null)
  const [editMode, setEditMode] = useState(false)
  const [editedBody, setEditedBody] = useState('')

  const templateTypes = [
    { value: 'job_outreach', label: '📬 Job Application Outreach', desc: 'Direct message to hiring manager' },
    { value: 'follow_up', label: '🔄 Follow-Up Email', desc: 'After application or interview' },
    { value: 'networking', label: '🤝 Networking Request', desc: 'Professional connection message' },
    { value: 'internship', label: '💬 Internship Inquiry', desc: 'Request for internship opportunity' },
    { value: 'rejection_response', label: '✍️ Rejection Response', desc: 'Graceful response to rejection' },
    { value: 'referral_request', label: '🎯 Referral Request', desc: 'Ask for internal referral' }
  ]

  const handleSubmit = async (e) => {
    e.preventDefault()
    setLoading(true)
    setError('')
    setResult(null)
    setEditMode(false)

    try {
      if (!formData.user_name || !formData.company_name || !formData.role) {
        throw new Error('Please fill in all required fields')
      }

      const response = await fetch(`${API_BASE}/email-template`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify({
          template_type: formData.template_type,
          user_name: formData.user_name,
          company_name: formData.company_name,
          role: formData.role,
          additional_context: formData.additional_context
        })
      })

      if (!response.ok) {
        const errorData = await response.json().catch(() => ({ detail: 'Failed to generate' }))
        throw new Error(errorData.detail || 'Failed to generate email')
      }
      const data = await response.json()
      setResult(data)
      setEditedBody(data.email_body)
    } catch (err) {
      setError(err.message)
    } finally {
      setLoading(false)
    }
  }

  const handleRegenerate = () => {
    setResult(null)
    setEditMode(false)
    handleSubmit({ preventDefault: () => {} })
  }

  const copyToClipboard = (text, label) => {
    navigator.clipboard.writeText(text)
    setCopied(label)
    setTimeout(() => setCopied(null), 2000)
  }

  const getTemplateIcon = (type) => {
    const icons = {
      job_outreach: '📬',
      follow_up: '🔄',
      networking: '🤝',
      internship: '💬',
      rejection_response: '✍️',
      referral_request: '🎯'
    }
    return icons[type] || '📧'
  }

  return (
    <ToolkitSection
      title="📧 Email Templates"
      description="Generate professional, personalized emails for your job search"
    >
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Input Form */}
        <motion.div
          className="bg-gray-800 bg-opacity-50 p-6 rounded-lg border border-gray-700"
          initial={{ opacity: 0, x: -20 }}
          animate={{ opacity: 1, x: 0 }}
          transition={{ duration: 0.3 }}
        >
          <h3 className="text-lg font-semibold text-white mb-4">Compose Email</h3>
          <form onSubmit={handleSubmit} className="space-y-4">
            <div>
              <label className="block text-sm font-medium text-gray-300 mb-2">Email Type *</label>
              <select
                value={formData.template_type}
                onChange={(e) => setFormData({...formData, template_type: e.target.value})}
                className="w-full px-4 py-2 bg-gray-700 border border-gray-600 rounded text-white focus:outline-none focus:border-blue-500 focus:ring-1 focus:ring-blue-500/50"
              >
                {templateTypes.map((type) => (
                  <option key={type.value} value={type.value}>
                    {type.label}
                  </option>
                ))}
              </select>
              <p className="text-xs text-gray-400 mt-1">
                {templateTypes.find(t => t.value === formData.template_type)?.desc}
              </p>
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-300 mb-2">Your Name *</label>
              <input
                type="text"
                value={formData.user_name}
                onChange={(e) => setFormData({...formData, user_name: e.target.value})}
                placeholder="John Doe"
                className="w-full px-4 py-2 bg-gray-700 border border-gray-600 rounded text-white placeholder-gray-400 focus:outline-none focus:border-blue-500"
                required
              />
            </div>

            <div className="grid grid-cols-2 gap-3">
              <div>
                <label className="block text-sm font-medium text-gray-300 mb-2">Company *</label>
                <input
                  type="text"
                  value={formData.company_name}
                  onChange={(e) => setFormData({...formData, company_name: e.target.value})}
                  placeholder="TechCorp"
                  className="w-full px-4 py-2 bg-gray-700 border border-gray-600 rounded text-white placeholder-gray-400 focus:outline-none focus:border-blue-500"
                  required
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-300 mb-2">Role *</label>
                <input
                  type="text"
                  value={formData.role}
                  onChange={(e) => setFormData({...formData, role: e.target.value})}
                  placeholder="Engineer, Manager"
                  className="w-full px-4 py-2 bg-gray-700 border border-gray-600 rounded text-white placeholder-gray-400 focus:outline-none focus:border-blue-500"
                  required
                />
              </div>
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-300 mb-2">Additional Context</label>
              <textarea
                value={formData.additional_context}
                onChange={(e) => setFormData({...formData, additional_context: e.target.value})}
                placeholder="Any specific details to personalize? (optional)"
                rows="2"
                className="w-full px-4 py-2 bg-gray-700 border border-gray-600 rounded text-white placeholder-gray-400 focus:outline-none focus:border-blue-500"
              />
            </div>

            <div className="flex gap-2 pt-2">
              <motion.button
                type="submit"
                disabled={loading}
                whileHover={{ scale: 1.02 }}
                whileTap={{ scale: 0.98 }}
                className="flex-1 px-4 py-2 bg-gradient-to-r from-blue-500 to-blue-600 hover:from-blue-600 hover:to-blue-700 text-white rounded font-medium transition-all disabled:opacity-50 disabled:cursor-not-allowed"
              >
                {loading ? (
                  <span className="flex items-center justify-center gap-2">
                    <div className="w-4 h-4 border-2 border-blue-200 border-t-white rounded-full animate-spin" />
                    Generating...
                  </span>
                ) : (
                  '✨ Generate Email'
                )}
              </motion.button>
              {result && (
                <motion.button
                  type="button"
                  onClick={handleRegenerate}
                  className="px-4 py-2 bg-gray-700 hover:bg-gray-600 text-white rounded font-medium transition-colors"
                  whileHover={{ scale: 1.02 }}
                  whileTap={{ scale: 0.98 }}
                >
                  🔄
                </motion.button>
              )}
            </div>

            {error && (
              <motion.div
                className="p-3 bg-red-500/20 border border-red-500/50 rounded text-red-300 text-sm"
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
              >
                {error}
              </motion.div>
            )}
          </form>
        </motion.div>

        {/* Email Preview */}
        <AnimatePresence mode="wait">
          {result ? (
            <motion.div
              className="space-y-4"
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: -20 }}
            >
              {/* Email Type Badge */}
              <motion.div
                className="flex gap-2 items-center p-3 bg-gradient-to-r from-blue-500/20 to-purple-500/20 rounded-lg border border-blue-500/30"
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
              >
                <span className="text-2xl">{getTemplateIcon(formData.template_type)}</span>
                <div>
                  <p className="text-xs text-gray-400">Email Type</p>
                  <p className="text-sm font-semibold text-white">
                    {templateTypes.find(t => t.value === formData.template_type)?.label}
                  </p>
                </div>
              </motion.div>

              {/* Subject Line */}
              <motion.div
                className="bg-gray-800/50 rounded-lg border border-gray-700 p-4 space-y-3"
                initial={{ opacity: 0, y: 10 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: 0.1 }}
              >
                <div>
                  <p className="text-xs text-gray-400 font-semibold mb-1">SUBJECT LINE</p>
                  <p className="text-white font-semibold text-lg leading-relaxed">
                    {result.subject_line}
                  </p>
                </div>
                <motion.button
                  onClick={() => copyToClipboard(result.subject_line, 'subject')}
                  className={`text-sm font-medium px-3 py-1 rounded transition-all ${
                    copied === 'subject'
                      ? 'bg-green-500/20 text-green-400'
                      : 'bg-blue-500/20 text-blue-400 hover:bg-blue-500/30'
                  }`}
                  whileHover={{ scale: 1.05 }}
                >
                  {copied === 'subject' ? '✓ Copied!' : '📋 Copy Subject'}
                </motion.button>
              </motion.div>

              {/* Email Body */}
              <motion.div
                className="bg-gradient-to-br from-blue-500/10 to-purple-500/10 rounded-lg border border-blue-500/30 p-4 space-y-3"
                initial={{ opacity: 0, y: 10 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: 0.2 }}
              >
                <div className="flex justify-between items-center">
                  <p className="text-xs text-gray-400 font-semibold">EMAIL BODY</p>
                  <button
                    onClick={() => setEditMode(!editMode)}
                    className="text-xs text-blue-400 hover:text-blue-300 transition-colors"
                  >
                    {editMode ? '✓ Done' : '✏️ Edit'}
                  </button>
                </div>

                {editMode ? (
                  <textarea
                    value={editedBody}
                    onChange={(e) => setEditedBody(e.target.value)}
                    className="w-full px-3 py-2 bg-gray-700 border border-gray-600 rounded text-white text-sm leading-relaxed focus:outline-none focus:border-blue-500 min-h-48"
                  />
                ) : (
                  <p className="text-gray-300 text-sm leading-relaxed whitespace-pre-wrap bg-gray-800/30 p-3 rounded max-h-48 overflow-y-auto">
                    {result.email_body}
                  </p>
                )}

                <div className="flex gap-2">
                  <motion.button
                    onClick={() => copyToClipboard(editMode ? editedBody : result.email_body, 'body')}
                    className={`flex-1 text-sm font-medium px-3 py-2 rounded transition-all ${
                      copied === 'body'
                        ? 'bg-green-500/20 text-green-400'
                        : 'bg-blue-500/20 text-blue-400 hover:bg-blue-500/30'
                    }`}
                    whileHover={{ scale: 1.02 }}
                  >
                    {copied === 'body' ? '✓ Copied!' : '📋 Copy Body'}
                  </motion.button>
                  <motion.button
                    onClick={() => copyToClipboard(`${result.subject_line}\n\n${editMode ? editedBody : result.email_body}`, 'full')}
                    className={`flex-1 text-sm font-medium px-3 py-2 rounded transition-all ${
                      copied === 'full'
                        ? 'bg-green-500/20 text-green-400'
                        : 'bg-purple-500/20 text-purple-400 hover:bg-purple-500/30'
                    }`}
                    whileHover={{ scale: 1.02 }}
                  >
                    {copied === 'full' ? '✓ All Copied!' : '📧 Copy All'}
                  </motion.button>
                </div>
              </motion.div>

              {/* Tips */}
              {result.tips && (
                <motion.div
                  className="bg-gray-800/30 rounded-lg border border-gray-700 p-4"
                  initial={{ opacity: 0 }}
                  animate={{ opacity: 1 }}
                  transition={{ delay: 0.3 }}
                >
                  <p className="text-sm font-semibold text-white mb-2">💡 Tips for Success</p>
                  <ul className="space-y-1">
                    {result.tips.slice(0, 3).map((tip, i) => (
                      <li key={i} className="text-xs text-gray-300">
                        <span className="text-blue-400 mr-2">→</span>{tip}
                      </li>
                    ))}
                  </ul>
                </motion.div>
              )}
            </motion.div>
          ) : (
            !result && !loading && (
              <motion.div
                className="flex items-center justify-center h-96 text-center text-gray-400"
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
              >
                <div>
                  <p className="text-4xl mb-2">📧</p>
                  <p>Fill in the form and generate your professional email</p>
                </div>
              </motion.div>
            )
          )}
        </AnimatePresence>
      </div>
    </ToolkitSection>
  )
}

// Portfolio Showcase
const PortfolioShowcase = () => {
  const [portfolioItems, setPortfolioItems] = useState([
    {
      id: 1,
      title: 'Resume Analyzer AI',
      description: 'Advanced AI-powered resume analysis with real-time feedback and optimization suggestions',
      technologies: ['React', 'FastAPI', 'Machine Learning', 'TensorFlow'],
      github_link: 'https://github.com/example/resume-analyzer',
      demo_link: 'https://resumeiq.demo',
      domain: 'AI/ML'
    },
    {
      id: 2,
      title: 'E-commerce Platform',
      description: 'Full-stack e-commerce solution with payment integration and inventory management',
      technologies: ['React', 'Node.js', 'MongoDB', 'Stripe'],
      github_link: 'https://github.com/example/ecommerce',
      demo_link: 'https://ecommerce.demo',
      domain: 'Web Development'
    },
    {
      id: 3,
      title: 'Data Analytics Dashboard',
      description: 'Real-time analytics dashboard with interactive visualizations and insights',
      technologies: ['React', 'D3.js', 'Python', 'PostgreSQL'],
      github_link: 'https://github.com/example/analytics',
      demo_link: 'https://analytics.demo',
      domain: 'Data Analytics'
    }
  ])

  const [selectedDomain, setSelectedDomain] = useState(null)
  const [showForm, setShowForm] = useState(false)
  const [newProject, setNewProject] = useState({
    title: '',
    description: '',
    technologies: '',
    github_link: '',
    demo_link: '',
    domain: 'Web Development'
  })

  const domains = ['All', 'AI/ML', 'Web Development', 'Data Analytics']
  const filteredItems = selectedDomain && selectedDomain !== 'All'
    ? portfolioItems.filter(item => item.domain === selectedDomain)
    : portfolioItems

  const handleAddProject = (e) => {
    e.preventDefault()
    const techs = newProject.technologies
      .split(',')
      .map(t => t.trim())
      .filter(t => t)

    setPortfolioItems([...portfolioItems, {
      id: portfolioItems.length + 1,
      title: newProject.title,
      description: newProject.description,
      technologies: techs,
      github_link: newProject.github_link,
      demo_link: newProject.demo_link,
      domain: newProject.domain
    }])

    setNewProject({
      title: '',
      description: '',
      technologies: '',
      github_link: '',
      demo_link: '',
      domain: 'Web Development'
    })
    setShowForm(false)
  }

  return (
    <ToolkitSection
      title="🎁 Portfolio Showcase"
      description="Display your professional achievements, projects, and certifications"
    >
      {/* Domain Filter */}
      <motion.div
        className="flex gap-2 flex-wrap mb-6"
        initial={{ opacity: 0, y: -10 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.3 }}
      >
        {domains.map((domain) => (
          <motion.button
            key={domain}
            onClick={() => setSelectedDomain(domain === 'All' ? null : domain)}
            className={`px-4 py-2 rounded-lg text-sm font-medium transition-all ${
              (domain === 'All' && !selectedDomain) || selectedDomain === domain
                ? 'bg-blue-500 text-white'
                : 'bg-gray-700 text-gray-300 hover:bg-gray-600'
            }`}
            whileHover={{ scale: 1.05 }}
            whileTap={{ scale: 0.98 }}
          >
            {domain}
          </motion.button>
        ))}
      </motion.div>

      {/* Add Project Button */}
      <motion.button
        onClick={() => setShowForm(!showForm)}
        className="mb-6 px-4 py-2 bg-blue-500 hover:bg-blue-600 text-white rounded font-medium transition-colors"
        whileHover={{ scale: 1.05 }}
        whileTap={{ scale: 0.98 }}
      >
        {showForm ? '✕ Cancel' : '+ Add Project'}
      </motion.button>

      {/* Add Project Form */}
      <AnimatePresence>
        {showForm && (
          <motion.div
            className="bg-gray-800 bg-opacity-50 p-6 rounded-lg border border-gray-700 mb-6"
            initial={{ opacity: 0, y: -20 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: -20 }}
          >
            <h3 className="text-lg font-semibold text-white mb-4">Add New Project</h3>
            <form onSubmit={handleAddProject} className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <input
                type="text"
                placeholder="Project Title"
                value={newProject.title}
                onChange={(e) => setNewProject({...newProject, title: e.target.value})}
                className="px-4 py-2 bg-gray-700 border border-gray-600 rounded text-white placeholder-gray-400 focus:outline-none focus:border-blue-500 md:col-span-2"
                required
              />

              <textarea
                placeholder="Project Description"
                value={newProject.description}
                onChange={(e) => setNewProject({...newProject, description: e.target.value})}
                rows="3"
                className="px-4 py-2 bg-gray-700 border border-gray-600 rounded text-white placeholder-gray-400 focus:outline-none focus:border-blue-500 md:col-span-2"
                required
              />

              <input
                type="text"
                placeholder="Technologies (comma-separated)"
                value={newProject.technologies}
                onChange={(e) => setNewProject({...newProject, technologies: e.target.value})}
                className="px-4 py-2 bg-gray-700 border border-gray-600 rounded text-white placeholder-gray-400 focus:outline-none focus:border-blue-500 md:col-span-2"
                required
              />

              <input
                type="url"
                placeholder="GitHub Link (optional)"
                value={newProject.github_link}
                onChange={(e) => setNewProject({...newProject, github_link: e.target.value})}
                className="px-4 py-2 bg-gray-700 border border-gray-600 rounded text-white placeholder-gray-400 focus:outline-none focus:border-blue-500"
              />

              <input
                type="url"
                placeholder="Demo Link (optional)"
                value={newProject.demo_link}
                onChange={(e) => setNewProject({...newProject, demo_link: e.target.value})}
                className="px-4 py-2 bg-gray-700 border border-gray-600 rounded text-white placeholder-gray-400 focus:outline-none focus:border-blue-500"
              />

              <select
                value={newProject.domain}
                onChange={(e) => setNewProject({...newProject, domain: e.target.value})}
                className="px-4 py-2 bg-gray-700 border border-gray-600 rounded text-white focus:outline-none focus:border-blue-500 md:col-span-2"
              >
                <option value="Web Development">Web Development</option>
                <option value="AI/ML">AI/ML</option>
                <option value="Data Analytics">Data Analytics</option>
              </select>

              <button
                type="submit"
                className="px-4 py-2 bg-blue-500 hover:bg-blue-600 text-white rounded font-medium transition-colors md:col-span-2"
              >
                Add Project
              </button>
            </form>
          </motion.div>
        )}
      </AnimatePresence>

      {/* Portfolio Grid */}
      <motion.div
        className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6"
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ duration: 0.3, staggerChildren: 0.1 }}
      >
        {filteredItems.map((project) => (
          <motion.div
            key={project.id}
            className="bg-gray-800 bg-opacity-50 border border-gray-700 rounded-lg p-6 hover:border-blue-500 hover:bg-blue-500 hover:bg-opacity-5 transition-all group"
            whileHover={{ y: -8 }}
            initial={{ opacity: 0, y: 10 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.3 }}
          >
            <div className="flex justify-between items-start mb-3">
              <h3 className="text-lg font-semibold text-white group-hover:text-blue-400 transition-colors">{project.title}</h3>
              <span className="px-2 py-1 bg-blue-500 bg-opacity-20 text-blue-300 text-xs rounded-full border border-blue-500 border-opacity-30">
                {project.domain}
              </span>
            </div>

            <p className="text-gray-300 text-sm mb-4 line-clamp-2">{project.description}</p>

            <div className="mb-4">
              <p className="text-xs text-gray-400 mb-2">Technologies:</p>
              <div className="flex flex-wrap gap-2">
                {project.technologies.map((tech, i) => (
                  <span key={i} className="px-2 py-1 bg-gray-700 text-gray-300 text-xs rounded">
                    {tech}
                  </span>
                ))}
              </div>
            </div>

            <div className="flex gap-2">
              {project.github_link && (
                <a
                  href={project.github_link}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="flex-1 px-3 py-2 bg-gray-700 hover:bg-gray-600 text-white text-sm rounded text-center transition-colors"
                >
                  GitHub
                </a>
              )}
              {project.demo_link && (
                <a
                  href={project.demo_link}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="flex-1 px-3 py-2 bg-blue-500 hover:bg-blue-600 text-white text-sm rounded text-center transition-colors"
                >
                  Demo
                </a>
              )}
            </div>
          </motion.div>
        ))}
      </motion.div>

      {filteredItems.length === 0 && (
        <motion.div
          className="text-center py-12"
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
        >
          <p className="text-gray-400 mb-4">No projects in this category yet</p>
          <button
            onClick={() => setShowForm(true)}
            className="px-4 py-2 bg-blue-500 hover:bg-blue-600 text-white rounded font-medium transition-colors"
          >
            Add your first project
          </button>
        </motion.div>
      )}
    </ToolkitSection>
  )
}
