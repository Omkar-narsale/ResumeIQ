import React, { useState } from 'react'
import { motion } from 'framer-motion'
import { Card, CardTitle, CardContent } from '../components/Card'
import { useApi } from '../hooks/useApi'
import { pageVariants, containerVariants, itemVariants, spinVariants } from '../components/animations'

export const KeywordOptimizer = () => {
  const [resume, setResume] = useState('')
  const [jobDesc, setJobDesc] = useState('')
  const [result, setResult] = useState(null)
  const { call, loading, error } = useApi()

  const handleOptimize = async () => {
    if (!resume.trim() || !jobDesc.trim()) {
      alert('Please fill in both fields')
      return
    }

    try {
      const data = await call('POST', '/api/optimize-keywords', {
        resume: resume.slice(0, 1000),
        job_description: jobDesc.slice(0, 1000)
      })
      setResult(data)
    } catch (err) {
      console.error('Optimization failed:', err)
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
        <CardTitle>🔑 Keyword Optimizer</CardTitle>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div>
            <label className="block text-sm font-medium mb-2">Your Resume:</label>
            <textarea
              value={resume}
              onChange={(e) => setResume(e.target.value.slice(0, 1000))}
              placeholder="Paste your resume..."
              className="w-full h-40 resize-none"
              maxLength={1000}
            />
            <p className="text-xs text-gray-400 mt-2">{resume.length}/1000 characters</p>
          </div>

          <div>
            <label className="block text-sm font-medium mb-2">Job Description:</label>
            <textarea
              value={jobDesc}
              onChange={(e) => setJobDesc(e.target.value.slice(0, 1000))}
              placeholder="Paste job description..."
              className="w-full h-40 resize-none"
              maxLength={1000}
            />
            <p className="text-xs text-gray-400 mt-2">{jobDesc.length}/1000 characters</p>
          </div>
        </div>

        <motion.button
          onClick={handleOptimize}
          disabled={loading}
          className="btn-primary mt-4"
          whileHover={{ scale: 1.05 }}
          whileTap={{ scale: 0.95 }}
        >
          {loading ? 'Optimizing...' : 'Optimize Keywords'}
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
              <CardTitle>📊 Keyword Statistics</CardTitle>
              <CardContent>
                <div className="space-y-3">
                  <div className="flex justify-between">
                    <span>Matched Keywords:</span>
                    <span className="text-green-400 font-bold">{result.keywords_matched}</span>
                  </div>
                  <div className="flex justify-between">
                    <span>Missing Keywords:</span>
                    <span className="text-red-400 font-bold">{result.keywords_missing}</span>
                  </div>
                </div>
              </CardContent>
            </Card>
          </motion.div>

          <motion.div variants={itemVariants}>
            <Card>
              <CardTitle>✅ Already Optimized</CardTitle>
              <CardContent>
                <div className="flex flex-wrap gap-2">
                  {result.optimized_keywords?.map((k, i) => (
                    <span key={i} className="bg-green-500 bg-opacity-20 text-green-300 px-3 py-1 rounded-full text-sm">
                      {k}
                    </span>
                  ))}
                </div>
              </CardContent>
            </Card>
          </motion.div>

          <motion.div variants={itemVariants} className="md:col-span-2">
            <Card>
              <CardTitle>🎯 Recommended Keywords to Add</CardTitle>
              <CardContent>
                <div className="flex flex-wrap gap-2">
                  {result.recommended_keywords?.map((k, i) => (
                    <span key={i} className="bg-blue-500 bg-opacity-20 text-blue-300 px-3 py-1 rounded-full text-sm">
                      + {k}
                    </span>
                  ))}
                </div>
              </CardContent>
            </Card>
          </motion.div>

          <motion.div variants={itemVariants} className="md:col-span-2">
            <Card>
              <CardTitle>📍 Placement Suggestions</CardTitle>
              <CardContent>
                <ul className="space-y-3">
                  {result.placement_suggestions?.map((s, i) => (
                    <li key={i} className="flex gap-3">
                      <span className="text-blue-400">→</span>
                      <span>{s}</span>
                    </li>
                  ))}
                </ul>
              </CardContent>
            </Card>
          </motion.div>

          <motion.div variants={itemVariants} className="md:col-span-2">
            <Card>
              <CardTitle>🚀 ATS Improvements</CardTitle>
              <CardContent>
                <ul className="space-y-3">
                  {result.ats_improvements?.map((s, i) => (
                    <li key={i} className="flex gap-3">
                      <span className="text-green-400">✓</span>
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
