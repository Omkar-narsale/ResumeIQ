import React, { useState } from 'react'
import { motion } from 'framer-motion'
import { Card, CardTitle, CardContent } from '../components/Card'
import { useApi } from '../hooks/useApi'
import { pageVariants, containerVariants, itemVariants, spinVariants } from '../components/animations'

export const ATSScore = () => {
  const [resume, setResume] = useState('')
  const [result, setResult] = useState(null)
  const { call, loading, error } = useApi()

  const handleCheck = async () => {
    if (!resume.trim()) {
      alert('Please paste your resume')
      return
    }

    try {
      const data = await call('POST', '/api/ats-score', {
        resume: resume.slice(0, 2000)
      })
      setResult(data)
    } catch (err) {
      console.error('ATS check failed:', err)
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
        <CardTitle>📋 ATS Score Checker</CardTitle>
        <label className="block text-sm font-medium mb-2">Your Resume:</label>
        <textarea
          value={resume}
          onChange={(e) => setResume(e.target.value.slice(0, 2000))}
          placeholder="Paste your resume here..."
          className="w-full h-48 resize-none"
          maxLength={2000}
        />
        <p className="text-xs text-gray-400 mt-2">{resume.length}/2000 characters</p>

        <motion.button
          onClick={handleCheck}
          disabled={loading}
          className="btn-primary mt-4"
          whileHover={{ scale: 1.05 }}
          whileTap={{ scale: 0.95 }}
        >
          {loading ? 'Checking...' : 'Check ATS Score'}
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
              <CardTitle>ATS Score</CardTitle>
              <div className="text-center py-8">
                <motion.div
                  className={`text-7xl font-bold mb-4 ${getScoreColor(result.ats_score)}`}
                  initial={{ scale: 0 }}
                  animate={{ scale: 1 }}
                  transition={{ delay: 0.3, type: 'spring' }}
                >
                  {result.ats_score}
                </motion.div>
                <div className="w-full bg-gray-700 h-4 rounded-full overflow-hidden">
                  <motion.div
                    className={`h-full ${getScoreColor(result.ats_score).replace('text', 'bg')}`}
                    initial={{ width: 0 }}
                    animate={{ width: `${result.ats_score}%` }}
                    transition={{ duration: 1 }}
                  />
                </div>
                <p className="text-gray-400 text-sm mt-4">
                  {result.ats_score >= 80 ? '✓ Excellent ATS compatibility' :
                   result.ats_score >= 60 ? '⚠ Good, but room for improvement' :
                   '✗ Needs significant improvements'}
                </p>
              </div>
            </Card>
          </motion.div>

          <motion.div variants={itemVariants}>
            <Card>
              <CardTitle>📝 Formatting Check</CardTitle>
              <CardContent>
                <ul className="space-y-2 text-sm">
                  <li className={result.formatting_check.has_contact_info ? 'text-green-400' : 'text-red-400'}>
                    {result.formatting_check.has_contact_info ? '✓' : '✗'} Contact Information
                  </li>
                  <li className={result.formatting_check.has_standard_sections ? 'text-green-400' : 'text-red-400'}>
                    {result.formatting_check.has_standard_sections ? '✓' : '✗'} Standard Sections
                  </li>
                  <li className={result.formatting_check.has_quantified_metrics ? 'text-green-400' : 'text-red-400'}>
                    {result.formatting_check.has_quantified_metrics ? '✓' : '✗'} Quantified Metrics
                  </li>
                  <li className="text-blue-400">
                    📊 {result.formatting_check.skills_detected} Skills Detected
                  </li>
                </ul>
              </CardContent>
            </Card>
          </motion.div>

          {result.issues.length > 0 && (
            <motion.div variants={itemVariants} className="md:col-span-2">
              <Card>
                <CardTitle>⚠️ Issues Found</CardTitle>
                <CardContent>
                  <ul className="space-y-2">
                    {result.issues.map((issue, i) => (
                      <li key={i} className="flex gap-3">
                        <span className="text-red-400">✗</span>
                        <span>{issue}</span>
                      </li>
                    ))}
                  </ul>
                </CardContent>
              </Card>
            </motion.div>
          )}

          <motion.div variants={itemVariants} className="md:col-span-2">
            <Card>
              <CardTitle>💡 Suggestions</CardTitle>
              <CardContent>
                <ul className="space-y-3">
                  {result.suggestions.map((s, i) => (
                    <li key={i} className="flex gap-3">
                      <span className="text-green-400">→</span>
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
