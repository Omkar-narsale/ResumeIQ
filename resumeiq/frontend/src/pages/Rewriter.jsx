import React, { useState, useEffect } from 'react'
import { motion } from 'framer-motion'
import { Card, CardTitle, CardContent } from '../components/Card'
import { useApi } from '../hooks/useApi'
import { useResume } from '../hooks/useResume'
import { pageVariants, containerVariants, itemVariants, spinVariants } from '../components/animations'

export const Rewriter = () => {
  const [resumeText, setResumeText] = useState('')
  const [result, setResult] = useState(null)
  const { call, loading, error } = useApi()
  const { resume } = useResume()

  useEffect(() => {
    if (resume) {
      setResumeText(resume)
    }
  }, [resume])

  const handleRewrite = async () => {
    if (!resumeText.trim()) {
      alert('Please upload a resume or enter text')
      return
    }

    try {
      const data = await call('POST', '/api/rewrite', { text: resumeText })
      setResult(data)
    } catch (err) {
      console.error('Rewrite failed:', err)
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
        <CardTitle>✍️ Resume Rewriter</CardTitle>
        <div className="space-y-4">
          <div>
            <label className="block text-sm font-medium mb-2">Your Resume:</label>
            <textarea
              value={resumeText}
              onChange={(e) => setResumeText(e.target.value)}
              placeholder={resume ? "Your uploaded resume is loaded..." : "Paste your resume for professional enhancement..."}
              className="w-full h-64 resize-none p-4 rounded-lg bg-gray-800 border border-gray-700 text-gray-300 focus:border-blue-500 focus:outline-none"
            />
            <p className="text-xs text-gray-400 mt-2">{resumeText.length} characters</p>
          </div>

          <motion.button
            onClick={handleRewrite}
            disabled={loading || !resumeText.trim()}
            className={`btn-primary ${!resumeText.trim() ? 'opacity-50 cursor-not-allowed' : ''}`}
            whileHover={resumeText.trim() ? { scale: 1.05 } : {}}
            whileTap={resumeText.trim() ? { scale: 0.95 } : {}}
          >
            {loading ? 'Rewriting...' : 'Rewrite Resume'}
          </motion.button>

          {error && (
            <motion.div
              className="bg-red-500 bg-opacity-20 border border-red-500 text-red-300 p-4 rounded-lg"
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
            >
              {error}
            </motion.div>
          )}
        </div>
      </Card>

      {loading && (
        <motion.div className="flex justify-center py-12" variants={spinVariants}>
          <motion.div
            className="w-12 h-12 border-4 border-blue-500 border-t-transparent rounded-full"
            animate={{ rotate: 360 }}
            transition={{ duration: 1, repeat: Infinity }}
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
          <motion.div variants={itemVariants} className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <Card>
              <CardTitle>📝 Original</CardTitle>
              <CardContent>
                <p className="text-gray-300 text-sm leading-relaxed whitespace-pre-wrap max-h-96 overflow-y-auto">
                  {result.original}
                </p>
              </CardContent>
            </Card>

            <Card>
              <CardTitle>✨ Improved Version</CardTitle>
              <CardContent>
                <p className="text-gray-300 text-sm leading-relaxed whitespace-pre-wrap max-h-96 overflow-y-auto">
                  {result.rewritten}
                </p>
              </CardContent>
            </Card>
          </motion.div>

          <motion.div variants={itemVariants}>
            <Card>
              <CardTitle>🎯 Improvements Made</CardTitle>
              <CardContent>
                <ul className="space-y-3">
                  {result.improvements?.map((imp, i) => (
                    <li key={i} className="flex gap-3">
                      <span className="text-green-400 font-bold min-w-6">{i + 1}.</span>
                      <span className="text-gray-300">{imp}</span>
                    </li>
                  ))}
                </ul>
              </CardContent>
            </Card>
          </motion.div>

          <motion.div variants={itemVariants} className="flex gap-3">
            <motion.button
              onClick={() => {
                navigator.clipboard.writeText(result.rewritten)
                alert('Copied to clipboard!')
              }}
              className="btn-primary"
              whileHover={{ scale: 1.05 }}
              whileTap={{ scale: 0.95 }}
            >
              📋 Copy Rewritten Version
            </motion.button>
            <motion.button
              onClick={() => setResult(null)}
              className="btn-secondary"
              whileHover={{ scale: 1.05 }}
              whileTap={{ scale: 0.95 }}
            >
              ← Rewrite Again
            </motion.button>
          </motion.div>
        </motion.div>
      )}
    </motion.div>
  )
}
