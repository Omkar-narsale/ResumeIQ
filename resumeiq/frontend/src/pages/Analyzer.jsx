import React, { useState } from 'react'
import { motion } from 'framer-motion'
import { Card, CardTitle, CardContent } from '../components/Card'
import { useApi } from '../hooks/useApi'
import { pageVariants, containerVariants, itemVariants, spinVariants } from '../components/animations'

export const Analyzer = () => {
  const [resumeText, setResumeText] = useState('')
  const [result, setResult] = useState(null)
  const { call, loading, error } = useApi()

  const handleAnalyze = async () => {
    if (!resumeText.trim()) {
      alert('Please enter resume text')
      return
    }

    try {
      const data = await call('POST', '/api/analyze', { text: resumeText })
      setResult(data)
    } catch (err) {
      console.error('Analysis failed:', err)
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
        <CardTitle>📄 Resume Analyzer</CardTitle>
        <div className="space-y-4">
          <div>
            <label className="block text-sm font-medium mb-2">Paste your resume:</label>
            <textarea
              value={resumeText}
              onChange={(e) => setResumeText(e.target.value.slice(0, 10000))}
              placeholder="Paste your resume here (max 10,000 characters)..."
              className="w-full h-40 resize-none"
              maxLength={10000}
            />
            <p className="text-xs text-gray-400 mt-2">{resumeText.length}/10000 characters</p>
          </div>

          <motion.button
            onClick={handleAnalyze}
            disabled={loading}
            className="btn-primary"
            whileHover={{ scale: 1.05 }}
            whileTap={{ scale: 0.95 }}
          >
            {loading ? 'Analyzing...' : 'Analyze Resume'}
          </motion.button>

          {error && (
            <motion.div
              className="bg-red-500 bg-opacity-20 border border-red-500 text-red-300 p-3 rounded-lg"
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
            >
              {error}
            </motion.div>
          )}
        </div>
      </Card>

      {loading && (
        <motion.div className="flex justify-center py-8" variants={spinVariants}>
          <motion.div
            className="w-12 h-12 border-4 border-blue-500 border-t-transparent rounded-full"
            animate="rotate"
          />
        </motion.div>
      )}

      {result && (
        <motion.div className="space-y-6">
          {/* Score Card - Enhanced */}
          <motion.div
            initial={{ opacity: 0, scale: 0.9 }}
            animate={{ opacity: 1, scale: 1 }}
            className="bg-gradient-to-br from-blue-600 to-purple-600 rounded-lg p-8 text-white"
          >
            <div className="flex items-center justify-between">
              <div>
                <p className="text-gray-200 text-sm mb-2">Resume Score</p>
                <div className="flex items-baseline gap-2">
                  <span className="text-5xl font-bold">{result.score}</span>
                  <span className="text-2xl text-gray-300">/10</span>
                </div>
              </div>
              <div className="text-right">
                <div className="text-6xl font-bold text-yellow-300">{(result.score * 10).toFixed(0)}%</div>
                <div className="text-sm text-gray-200 mt-2">
                  {result.score >= 8 && "Excellent!"}
                  {result.score >= 6 && result.score < 8 && "Good - Room for improvement"}
                  {result.score < 6 && "Needs work - Follow suggestions"}
                </div>
              </div>
            </div>
            <div className="mt-4 bg-black bg-opacity-30 rounded-full h-2">
              <div
                className="bg-yellow-400 h-full rounded-full transition-all duration-500"
                style={{ width: `${result.score * 10}%` }}
              />
            </div>
          </motion.div>

          {/* Main Grid */}
          <motion.div
            className="grid grid-cols-1 md:grid-cols-2 gap-6"
            variants={containerVariants}
            initial="hidden"
            animate="visible"
          >
            {/* Strengths */}
            <motion.div variants={itemVariants}>
              <Card>
                <CardTitle>💪 Strengths</CardTitle>
                <CardContent>
                  <ul className="space-y-2">
                    {result.strengths?.map((s, i) => (
                      <li key={i} className="text-green-400 flex items-start gap-2">
                        <span>✓</span>
                        <span>{s.replace('✓ ', '')}</span>
                      </li>
                    ))}
                  </ul>
                </CardContent>
              </Card>
            </motion.div>

            {/* Weaknesses */}
            <motion.div variants={itemVariants}>
              <Card>
                <CardTitle>⚠️ Weaknesses</CardTitle>
                <CardContent>
                  <ul className="space-y-2">
                    {result.weaknesses?.map((w, i) => (
                      <li key={i} className="text-red-400 flex items-start gap-2">
                        <span>✗</span>
                        <span>{w.replace('✗ ', '')}</span>
                      </li>
                    ))}
                  </ul>
                </CardContent>
              </Card>
            </motion.div>

            {/* Skills Matched */}
            <motion.div variants={itemVariants}>
              <Card>
                <CardTitle>✅ Skills Found</CardTitle>
                <CardContent>
                  <div className="flex flex-wrap gap-2">
                    {result.skills_matched?.slice(0, 8).map((s, i) => (
                      <span key={i} className="bg-green-500 bg-opacity-20 text-green-400 px-3 py-1 rounded-full text-sm border border-green-500 border-opacity-50">
                        {s}
                      </span>
                    ))}
                  </div>
                  {result.skills_matched?.length > 8 && (
                    <p className="text-xs text-gray-400 mt-2">+{result.skills_matched.length - 8} more skills</p>
                  )}
                </CardContent>
              </Card>
            </motion.div>

            {/* Priority Skills */}
            <motion.div variants={itemVariants}>
              <Card>
                <CardTitle>🎯 Top Priority Skills</CardTitle>
                <CardContent>
                  <div className="space-y-2">
                    {result.priority_skills?.map((s, i) => (
                      <div key={i} className="bg-blue-500 bg-opacity-20 px-4 py-2 rounded-lg border-l-4 border-blue-500">
                        <span className="text-blue-300 font-medium">{s}</span>
                      </div>
                    ))}
                  </div>
                </CardContent>
              </Card>
            </motion.div>

            {/* Skills to Learn */}
            <motion.div variants={itemVariants} className="md:col-span-1">
              <Card>
                <CardTitle>📚 Skills to Learn</CardTitle>
                <CardContent>
                  <div className="flex flex-wrap gap-2">
                    {result.skills_missing?.slice(0, 6).map((s, i) => (
                      <span key={i} className="bg-orange-500 bg-opacity-20 text-orange-400 px-3 py-1 rounded-full text-sm border border-orange-500 border-opacity-50">
                        {s}
                      </span>
                    ))}
                  </div>
                </CardContent>
              </Card>
            </motion.div>

            {/* Suggestions */}
            <motion.div variants={itemVariants} className="md:col-span-2">
              <Card>
                <CardTitle>💡 Improvements Needed</CardTitle>
                <CardContent>
                  <div className="space-y-3">
                    {result.suggestions?.map((s, i) => (
                      <div key={i} className="flex gap-3 p-3 bg-gray-800 bg-opacity-50 rounded-lg">
                        <span className="text-yellow-400 font-bold">{i + 1}.</span>
                        <span className="text-gray-200">{s}</span>
                      </div>
                    ))}
                  </div>
                </CardContent>
              </Card>
            </motion.div>
          </motion.div>
        </motion.div>
      )}
    </motion.div>
  )
}
