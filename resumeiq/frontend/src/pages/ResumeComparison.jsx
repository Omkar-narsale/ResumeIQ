import React, { useState } from 'react'
import { motion } from 'framer-motion'
import { Card, CardTitle, CardContent } from '../components/Card'
import { useApi } from '../hooks/useApi'
import { pageVariants, containerVariants, itemVariants, spinVariants } from '../components/animations'

export const ResumeComparison = () => {
  const [resume1, setResume1] = useState('')
  const [resume2, setResume2] = useState('')
  const [result, setResult] = useState(null)
  const { call, loading, error } = useApi()

  const handleCompare = async () => {
    if (!resume1.trim() || !resume2.trim()) {
      alert('Please fill in both resume fields')
      return
    }

    try {
      const data = await call('POST', '/api/compare-resumes', {
        resume1: resume1.slice(0, 1500),
        resume2: resume2.slice(0, 1500)
      })
      setResult(data)
    } catch (err) {
      console.error('Comparison failed:', err)
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
        <CardTitle>📊 Resume Comparison</CardTitle>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div>
            <label className="block text-sm font-medium mb-2">Resume 1:</label>
            <textarea
              value={resume1}
              onChange={(e) => setResume1(e.target.value.slice(0, 1500))}
              placeholder="Paste first resume..."
              className="w-full h-40 resize-none"
              maxLength={1500}
            />
            <p className="text-xs text-gray-400 mt-2">{resume1.length}/1500 characters</p>
          </div>

          <div>
            <label className="block text-sm font-medium mb-2">Resume 2:</label>
            <textarea
              value={resume2}
              onChange={(e) => setResume2(e.target.value.slice(0, 1500))}
              placeholder="Paste second resume..."
              className="w-full h-40 resize-none"
              maxLength={1500}
            />
            <p className="text-xs text-gray-400 mt-2">{resume2.length}/1500 characters</p>
          </div>
        </div>

        <motion.button
          onClick={handleCompare}
          disabled={loading}
          className="btn-primary mt-4"
          whileHover={{ scale: 1.05 }}
          whileTap={{ scale: 0.95 }}
        >
          {loading ? 'Comparing...' : 'Compare Resumes'}
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
          className="space-y-6"
          variants={containerVariants}
          initial="hidden"
          animate="visible"
        >
          <motion.div variants={itemVariants}>
            <Card>
              <CardTitle>📋 Summary</CardTitle>
              <CardContent>
                <p className="text-gray-300">{result.comparison_summary}</p>
              </CardContent>
            </Card>
          </motion.div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <motion.div variants={itemVariants}>
              <Card>
                <CardTitle>💪 Resume 1 Strengths</CardTitle>
                <CardContent>
                  <ul className="space-y-2">
                    {result.resume1_strengths?.map((s, i) => (
                      <li key={i} className="flex gap-3">
                        <span className="text-green-400">✓</span>
                        <span className="text-sm">{s}</span>
                      </li>
                    ))}
                  </ul>
                </CardContent>
              </Card>
            </motion.div>

            <motion.div variants={itemVariants}>
              <Card>
                <CardTitle>💪 Resume 2 Strengths</CardTitle>
                <CardContent>
                  <ul className="space-y-2">
                    {result.resume2_strengths?.map((s, i) => (
                      <li key={i} className="flex gap-3">
                        <span className="text-green-400">✓</span>
                        <span className="text-sm">{s}</span>
                      </li>
                    ))}
                  </ul>
                </CardContent>
              </Card>
            </motion.div>
          </div>

          <motion.div variants={itemVariants}>
            <Card>
              <CardTitle>📊 Length Comparison</CardTitle>
              <CardContent>
                <div className="grid grid-cols-2 gap-4">
                  <div>
                    <div className="text-2xl font-bold text-blue-400">
                      {result.length_comparison?.resume1}
                    </div>
                    <p className="text-gray-400 text-sm">characters</p>
                  </div>
                  <div>
                    <div className="text-2xl font-bold text-purple-400">
                      {result.length_comparison?.resume2}
                    </div>
                    <p className="text-gray-400 text-sm">characters</p>
                  </div>
                </div>
              </CardContent>
            </Card>
          </motion.div>

          <motion.div variants={itemVariants}>
            <Card>
              <CardTitle>🔧 Skills Count</CardTitle>
              <CardContent>
                <div className="grid grid-cols-2 gap-4">
                  <div>
                    <div className="text-2xl font-bold text-green-400">
                      {result.skills_comparison?.resume1_total}
                    </div>
                    <p className="text-gray-400 text-sm">Resume 1 Skills</p>
                  </div>
                  <div>
                    <div className="text-2xl font-bold text-green-400">
                      {result.skills_comparison?.resume2_total}
                    </div>
                    <p className="text-gray-400 text-sm">Resume 2 Skills</p>
                  </div>
                </div>
              </CardContent>
            </Card>
          </motion.div>

          {result.common_skills?.length > 0 && (
            <motion.div variants={itemVariants}>
              <Card>
                <CardTitle>🔗 Common Skills</CardTitle>
                <CardContent>
                  <div className="flex flex-wrap gap-2">
                    {result.common_skills?.map((s, i) => (
                      <span key={i} className="bg-blue-500 bg-opacity-20 text-blue-300 px-3 py-1 rounded-full text-sm">
                        {s}
                      </span>
                    ))}
                  </div>
                </CardContent>
              </Card>
            </motion.div>
          )}

          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            {result.resume1_unique?.length > 0 && (
              <motion.div variants={itemVariants}>
                <Card>
                  <CardTitle>⭐ Resume 1 Unique</CardTitle>
                  <CardContent>
                    <div className="flex flex-wrap gap-2">
                      {result.resume1_unique?.map((s, i) => (
                        <span key={i} className="bg-blue-500 bg-opacity-20 text-blue-300 px-2 py-1 rounded text-xs">
                          {s}
                        </span>
                      ))}
                    </div>
                  </CardContent>
                </Card>
              </motion.div>
            )}

            {result.resume2_unique?.length > 0 && (
              <motion.div variants={itemVariants}>
                <Card>
                  <CardTitle>⭐ Resume 2 Unique</CardTitle>
                  <CardContent>
                    <div className="flex flex-wrap gap-2">
                      {result.resume2_unique?.map((s, i) => (
                        <span key={i} className="bg-purple-500 bg-opacity-20 text-purple-300 px-2 py-1 rounded text-xs">
                          {s}
                        </span>
                      ))}
                    </div>
                  </CardContent>
                </Card>
              </motion.div>
            )}
          </div>
        </motion.div>
      )}
    </motion.div>
  )
}
