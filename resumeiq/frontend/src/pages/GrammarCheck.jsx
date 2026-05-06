import React, { useState } from 'react'
import { motion } from 'framer-motion'
import { Card, CardTitle, CardContent } from '../components/Card'
import { useApi } from '../hooks/useApi'
import { pageVariants, containerVariants, itemVariants, spinVariants } from '../components/animations'

export const GrammarCheck = () => {
  const [resume, setResume] = useState('')
  const [result, setResult] = useState(null)
  const { call, loading, error } = useApi()

  const handleCheck = async () => {
    if (!resume.trim()) {
      alert('Please paste your resume')
      return
    }

    try {
      const data = await call('POST', '/api/grammar-check', {
        resume: resume.slice(0, 3000)
      })
      setResult(data)
    } catch (err) {
      console.error('Grammar check failed:', err)
    }
  }

  const getScoreColor = (score) => {
    if (score >= 80) return 'text-green-400'
    if (score >= 60) return 'text-yellow-400'
    return 'text-red-400'
  }

  return (
    <motion.div
      className="space-y-6"
      variants={pageVariants}
      initial="hidden"
      animate="visible"
    >
      <Card>
        <CardTitle>✏️ Grammar & Spell Check</CardTitle>
        <label className="block text-sm font-medium mb-2">Your Resume:</label>
        <textarea
          value={resume}
          onChange={(e) => setResume(e.target.value.slice(0, 3000))}
          placeholder="Paste your resume here..."
          className="w-full h-48 resize-none"
          maxLength={3000}
        />
        <p className="text-xs text-gray-400 mt-2">{resume.length}/3000 characters</p>

        <motion.button
          onClick={handleCheck}
          disabled={loading}
          className="btn-primary mt-4"
          whileHover={{ scale: 1.05 }}
          whileTap={{ scale: 0.95 }}
        >
          {loading ? 'Checking...' : 'Check Grammar'}
        </motion.button>

        {error && (
          <motion.div
            className="bg-red-500 bg-opacity-20 border border-red-500 text-red-300 p-3 rounded-lg mt-4"
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
          >
            {error}
          </motion.div>
        )}
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
              <CardTitle>📊 Grammar Score</CardTitle>
              <div className="text-center py-8">
                <motion.div
                  className={`text-7xl font-bold mb-4 ${getScoreColor(result.grammar_score)}`}
                  initial={{ scale: 0 }}
                  animate={{ scale: 1 }}
                  transition={{ delay: 0.3, type: 'spring' }}
                >
                  {Math.round(result.grammar_score)}
                </motion.div>
                <div className="w-full bg-gray-700 h-4 rounded-full overflow-hidden">
                  <motion.div
                    className={`h-full ${getScoreColor(result.grammar_score).replace('text', 'bg')}`}
                    initial={{ width: 0 }}
                    animate={{ width: `${result.grammar_score}%` }}
                    transition={{ duration: 1 }}
                  />
                </div>
                <p className="text-gray-400 text-sm mt-4 font-semibold">
                  {result.overall_feedback}
                </p>
              </div>
            </Card>
          </motion.div>

          <motion.div variants={itemVariants}>
            <Card>
              <CardTitle>🔍 Issues Found</CardTitle>
              <CardContent>
                <div className="space-y-2">
                  <div className="text-3xl font-bold text-red-400">
                    {result.issues_found}
                  </div>
                  <p className="text-gray-400 text-sm">
                    {result.issues_found === 0 ? 'Perfect! No issues found.' : `${result.issues_found} issue${result.issues_found !== 1 ? 's' : ''} detected`}
                  </p>
                </div>
              </CardContent>
            </Card>
          </motion.div>

          {result.issues && result.issues.length > 0 && (
            <motion.div variants={itemVariants} className="md:col-span-2">
              <Card>
                <CardTitle>⚠️ Issues Detected</CardTitle>
                <CardContent>
                  <ul className="space-y-3">
                    {result.issues.map((issue, i) => (
                      <li key={i} className="border-l-4 border-red-500 pl-3">
                        <div className="text-red-400 font-semibold text-sm">{issue.type}</div>
                        <div className="text-gray-300 text-sm">"{issue.text}"</div>
                        <div className="text-gray-500 text-xs">{issue.suggestion}</div>
                      </li>
                    ))}
                  </ul>
                </CardContent>
              </Card>
            </motion.div>
          )}

          {result.suggestions && result.suggestions.length > 0 && (
            <motion.div variants={itemVariants} className="md:col-span-2">
              <Card>
                <CardTitle>💡 Improvement Suggestions</CardTitle>
                <CardContent>
                  <ul className="space-y-2">
                    {result.suggestions.map((s, i) => (
                      <li key={i} className="flex gap-3">
                        <span className="text-yellow-400">→</span>
                        <span className="text-sm">{s}</span>
                      </li>
                    ))}
                  </ul>
                </CardContent>
              </Card>
            </motion.div>
          )}

          <motion.div variants={itemVariants} className="md:col-span-2">
            <Card>
              <CardTitle>📋 Quick Tips</CardTitle>
              <CardContent>
                <ul className="space-y-2 text-sm text-gray-300">
                  <li>✓ Use strong action verbs (Led, Developed, Implemented)</li>
                  <li>✓ Avoid passive voice when possible</li>
                  <li>✓ Be consistent with tense throughout</li>
                  <li>✓ Proofread multiple times before submitting</li>
                </ul>
              </CardContent>
            </Card>
          </motion.div>
        </motion.div>
      )}
    </motion.div>
  )
}
