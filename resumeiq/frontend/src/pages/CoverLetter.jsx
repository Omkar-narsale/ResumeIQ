import React, { useState } from 'react'
import { motion } from 'framer-motion'
import { Card, CardTitle, CardContent } from '../components/Card'
import { useApi } from '../hooks/useApi'
import { useResume } from '../hooks/useResume'
import { pageVariants, containerVariants, itemVariants } from '../components/animations'

export const CoverLetter = () => {
  const [jobDescription, setJobDescription] = useState('')
  const [result, setResult] = useState(null)
  const [copied, setCopied] = useState(false)
  const { resume } = useResume()
  const { call, loading, error } = useApi()

  const handleGenerate = async () => {
    if (!jobDescription.trim()) {
      alert('Please enter a job description')
      return
    }
    if (!resume) {
      alert('Please upload a resume first')
      return
    }

    try {
      const data = await call('POST', '/api/generate-cover-letter', {
        job_description: jobDescription.slice(0, 1000),
        resume: resume.slice(0, 1000)
      })
      setResult(data)
    } catch (err) {
      console.error('Generation failed:', err)
    }
  }

  const handleCopy = (text) => {
    navigator.clipboard.writeText(text)
    setCopied(true)
    setTimeout(() => setCopied(false), 2000)
  }

  return (
    <motion.div
      className="space-y-6"
      variants={pageVariants}
      initial="hidden"
      animate="visible"
    >
      <Card>
        <CardTitle>📝 Cover Letter Generator</CardTitle>
        <CardContent className="space-y-4">
          <div>
            <label className="block text-sm font-medium mb-2">Paste Job Description:</label>
            <textarea
              value={jobDescription}
              onChange={(e) => setJobDescription(e.target.value.slice(0, 1000))}
              placeholder="Paste the full job description here. Be as detailed as possible..."
              className="w-full h-40 resize-none bg-gray-800 border border-gray-700 rounded px-3 py-2 text-white"
              maxLength={1000}
            />
            <p className="text-xs text-gray-400 mt-2">{jobDescription.length}/1000 characters</p>
          </div>

          <motion.button
            onClick={handleGenerate}
            disabled={loading || !resume || !jobDescription.trim()}
            className="w-full btn-primary disabled:opacity-50 disabled:cursor-not-allowed"
            whileHover={{ scale: 1.05 }}
            whileTap={{ scale: 0.95 }}
          >
            {loading ? 'Generating...' : '✨ Generate Cover Letter'}
          </motion.button>

          {!resume && (
            <motion.div
              className="bg-orange-500 bg-opacity-20 border border-orange-500 text-orange-300 p-3 rounded-lg text-sm"
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
            >
              📄 Tip: Upload a resume first to get better-tailored cover letters
            </motion.div>
          )}

          {error && (
            <motion.div
              className="bg-red-500 bg-opacity-20 border border-red-500 text-red-300 p-3 rounded-lg"
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
            >
              {error}
            </motion.div>
          )}
        </CardContent>
      </Card>

      {result && (
        <motion.div
          className="space-y-6"
          variants={containerVariants}
          initial="hidden"
          animate="visible"
        >
          {/* Cover Letter */}
          <motion.div variants={itemVariants}>
            <Card>
              <CardTitle>✍️ Generated Cover Letter</CardTitle>
              <CardContent className="space-y-4">
                <div className="bg-gray-800 border border-gray-700 rounded p-6 whitespace-pre-wrap text-sm leading-relaxed max-h-96 overflow-y-auto">
                  {result.cover_letter}
                </div>
                <motion.button
                  onClick={() => handleCopy(result.cover_letter)}
                  className="w-full btn-primary"
                  whileHover={{ scale: 1.05 }}
                  whileTap={{ scale: 0.95 }}
                >
                  {copied ? '✓ Copied!' : '📋 Copy to Clipboard'}
                </motion.button>
              </CardContent>
            </Card>
          </motion.div>

          {/* Improvements */}
          <motion.div variants={itemVariants}>
            <Card>
              <CardTitle>💡 Key Improvements Applied</CardTitle>
              <CardContent>
                <ul className="space-y-3">
                  {result.improvements?.map((improvement, i) => (
                    <li key={i} className="flex gap-3">
                      <span className="text-green-400 font-bold">✓</span>
                      <span className="text-sm">{improvement}</span>
                    </li>
                  ))}
                </ul>
              </CardContent>
            </Card>
          </motion.div>

          {/* Tips */}
          <motion.div variants={itemVariants}>
            <Card>
              <CardTitle>🎯 Tips for Better Results</CardTitle>
              <CardContent>
                <ul className="space-y-2 text-sm text-gray-300">
                  <li>• Personalize the company name and specific role</li>
                  <li>• Include metrics and quantifiable achievements</li>
                  <li>• Address specific requirements from the job description</li>
                  <li>• Use professional tone with personality</li>
                  <li>• Keep it 3-4 paragraphs, focused and compelling</li>
                </ul>
              </CardContent>
            </Card>
          </motion.div>

          {/* Generate New */}
          <motion.button
            onClick={() => {
              setResult(null)
              setJobDescription('')
            }}
            className="w-full text-gray-400 hover:text-gray-300 text-sm py-2"
            whileHover={{ scale: 1.02 }}
          >
            Generate Another
          </motion.button>
        </motion.div>
      )}
    </motion.div>
  )
}
