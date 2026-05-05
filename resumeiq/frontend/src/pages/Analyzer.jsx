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
              onChange={(e) => setResumeText(e.target.value.slice(0, 1500))}
              placeholder="Paste your resume here (max 1500 characters)..."
              className="w-full h-40 resize-none"
              maxLength={1500}
            />
            <p className="text-xs text-gray-400 mt-2">{resumeText.length}/1500 characters</p>
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
        <motion.div
          className="grid grid-cols-1 md:grid-cols-2 gap-6"
          variants={containerVariants}
          initial="hidden"
          animate="visible"
        >
          <motion.div variants={itemVariants}>
            <Card>
              <CardTitle>Score: {result.score}/10</CardTitle>
              <div className="bg-gradient-to-r from-blue-500 to-blue-600 h-2 rounded-full mb-4" style={{width: `${result.score * 10}%`}} />
              <CardContent>
                <div className="text-3xl font-bold text-yellow-400">{(result.score * 10).toFixed(0)}%</div>
              </CardContent>
            </Card>
          </motion.div>

          <motion.div variants={itemVariants}>
            <Card>
              <CardTitle>💪 Strengths</CardTitle>
              <CardContent>
                <ul className="space-y-2">
                  {result.strengths?.slice(0, 3).map((s, i) => (
                    <li key={i} className="text-green-400">✓ {s}</li>
                  ))}
                </ul>
              </CardContent>
            </Card>
          </motion.div>

          <motion.div variants={itemVariants}>
            <Card>
              <CardTitle>⚠️ Weaknesses</CardTitle>
              <CardContent>
                <ul className="space-y-2">
                  {result.weaknesses?.slice(0, 3).map((w, i) => (
                    <li key={i} className="text-red-400">✗ {w}</li>
                  ))}
                </ul>
              </CardContent>
            </Card>
          </motion.div>

          <motion.div variants={itemVariants}>
            <Card>
              <CardTitle>🎯 Priority Skills</CardTitle>
              <CardContent>
                <div className="flex flex-wrap gap-2">
                  {result.priority_skills?.map((s, i) => (
                    <span key={i} className="bg-blue-500 bg-opacity-30 px-3 py-1 rounded-full text-sm">
                      {s}
                    </span>
                  ))}
                </div>
              </CardContent>
            </Card>
          </motion.div>

          <motion.div variants={itemVariants} className="md:col-span-2">
            <Card>
              <CardTitle>💡 Suggestions</CardTitle>
              <CardContent>
                <ul className="space-y-3">
                  {result.suggestions?.map((s, i) => (
                    <li key={i} className="flex gap-3">
                      <span className="text-blue-400">→</span>
                      <span>{s}</span>
                    </li>
                  ))}
                </ul>
              </CardContent>
            </Card>
          </motion.div>
        </motion.div>
      )}
    </motion.div>
  )
}
