import React, { useState } from 'react'
import { motion } from 'framer-motion'
import { Card, CardTitle, CardContent } from '../components/Card'
import { useResume } from '../hooks/useResume'
import { pageVariants, containerVariants, itemVariants } from '../components/animations'

export const ResumeUpload = () => {
  const { resume, resumes, autoAnalysis, uploadResume, selectResume, deleteResume, loading } = useResume()
  const [dragActive, setDragActive] = useState(false)
  const [error, setError] = useState('')

  const handleDrag = (e) => {
    e.preventDefault()
    e.stopPropagation()
    if (e.type === "dragenter" || e.type === "dragover") {
      setDragActive(true)
    } else if (e.type === "dragleave") {
      setDragActive(false)
    }
  }

  const handleDrop = (e) => {
    e.preventDefault()
    e.stopPropagation()
    setDragActive(false)

    const files = e.dataTransfer.files
    if (files && files[0]) {
      handleFile(files[0])
    }
  }

  const handleChange = (e) => {
    if (e.target.files && e.target.files[0]) {
      handleFile(e.target.files[0])
    }
  }

  const handleFile = async (file) => {
    setError('')
    if (!file.name.endsWith('.pdf')) {
      setError('Only PDF files are allowed')
      return
    }

    try {
      await uploadResume(file)
    } catch (err) {
      setError(err.message || 'Upload failed')
    }
  }

  return (
    <motion.div
      className="space-y-6"
      variants={pageVariants}
      initial="hidden"
      animate="visible"
    >
      {/* Upload Area */}
      <Card>
        <CardTitle>📂 Upload Your Resume</CardTitle>
        <motion.div
          className={`border-2 border-dashed rounded-lg p-12 text-center transition-all cursor-pointer ${
            dragActive
              ? 'border-blue-400 bg-blue-500 bg-opacity-10'
              : 'border-gray-600 hover:border-blue-400'
          }`}
          onDragEnter={handleDrag}
          onDragLeave={handleDrag}
          onDragOver={handleDrag}
          onDrop={handleDrop}
          whileHover={{ scale: 1.02 }}
        >
          <input
            type="file"
            id="file-input"
            accept=".pdf"
            onChange={handleChange}
            className="hidden"
            disabled={loading}
          />
          <label htmlFor="file-input" className="cursor-pointer">
            <motion.div
              initial={{ opacity: 0, y: -10 }}
              animate={{ opacity: 1, y: 0 }}
              className="space-y-3"
            >
              <div className="text-5xl">📄</div>
              <p className="text-xl font-semibold text-blue-400">
                Drag & drop your PDF resume
              </p>
              <p className="text-gray-400">or click to browse</p>
              <p className="text-xs text-gray-500">PDF format only (Auto-analysis will run after upload)</p>
            </motion.div>
          </label>
        </motion.div>

        {error && (
          <motion.div
            className="mt-4 bg-red-500 bg-opacity-20 border border-red-500 text-red-300 px-4 py-3 rounded-lg"
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
          >
            {error}
          </motion.div>
        )}

        {loading && (
          <motion.div className="mt-4 flex flex-col items-center justify-center gap-3">
            <motion.div
              className="w-10 h-10 border-4 border-blue-500 border-t-transparent rounded-full"
              animate={{ rotate: 360 }}
              transition={{ duration: 1, repeat: Infinity, ease: 'linear' }}
            />
            <p className="text-gray-400 text-sm">Processing your resume...</p>
          </motion.div>
        )}
      </Card>

      {/* Current Resume */}
      {resume && (
        <motion.div
          variants={containerVariants}
          initial="hidden"
          animate="visible"
          className="space-y-6"
        >
          <motion.div variants={itemVariants}>
            <Card>
              <CardTitle>✅ Resume Active</CardTitle>
              <CardContent>
                <div className="space-y-4">
                  <p className="text-green-400 font-semibold">Resume loaded successfully!</p>
                  <p className="text-gray-400 text-sm">All features are now unlocked. Your resume is being analyzed...</p>
                  <p className="text-xs text-gray-500 bg-gray-900 bg-opacity-50 p-3 rounded max-h-32 overflow-y-auto font-mono">
                    {resume.substring(0, 300)}...
                  </p>
                </div>
              </CardContent>
            </Card>
          </motion.div>

          {/* Auto-Analysis Results */}
          {autoAnalysis && (
            <motion.div variants={itemVariants}>
              <Card>
                <CardTitle>🎯 Quick Analysis</CardTitle>
                <CardContent>
                  <div className="space-y-6">
                    {/* Score */}
                    <div className="flex items-center gap-4">
                      <div className="w-16 h-16 rounded-full bg-blue-500 bg-opacity-20 border-2 border-blue-500 flex items-center justify-center">
                        <span className="text-2xl font-bold text-blue-400">{autoAnalysis.score}/10</span>
                      </div>
                      <div>
                        <p className="text-gray-400 text-sm">Resume Score</p>
                        <p className="text-gray-300 font-semibold">
                          {autoAnalysis.score >= 8 ? 'Excellent' : autoAnalysis.score >= 6 ? 'Good' : 'Needs Improvement'}
                        </p>
                      </div>
                    </div>

                    {/* Quick Stats */}
                    <div className="grid grid-cols-2 gap-4">
                      <div className="bg-gray-800 bg-opacity-50 p-3 rounded-lg">
                        <p className="text-xs text-gray-400">Strengths Found</p>
                        <p className="text-lg font-bold text-green-400">{autoAnalysis.strengths?.length || 0}</p>
                      </div>
                      <div className="bg-gray-800 bg-opacity-50 p-3 rounded-lg">
                        <p className="text-xs text-gray-400">Areas to Improve</p>
                        <p className="text-lg font-bold text-yellow-400">{autoAnalysis.weaknesses?.length || 0}</p>
                      </div>
                    </div>

                    {/* Skills */}
                    {autoAnalysis.skills_matched && autoAnalysis.skills_matched.length > 0 && (
                      <div>
                        <p className="text-sm font-semibold text-gray-300 mb-2">Detected Skills</p>
                        <div className="flex flex-wrap gap-2">
                          {autoAnalysis.skills_matched.slice(0, 5).map((skill, i) => (
                            <span key={i} className="text-xs bg-blue-500 bg-opacity-30 text-blue-300 px-3 py-1 rounded-full">
                              {skill}
                            </span>
                          ))}
                        </div>
                      </div>
                    )}

                    <p className="text-xs text-gray-500 text-center">
                      🔍 Full analysis available in the Resume Analyzer
                    </p>
                  </div>
                </CardContent>
              </Card>
            </motion.div>
          )}
        </motion.div>
      )}

      {/* Resume Library */}
      {resumes.length > 1 && (
        <motion.div variants={itemVariants}>
          <Card>
            <CardTitle>📚 Your Resumes ({resumes.length})</CardTitle>
            <CardContent>
              <div className="space-y-3">
                {resumes.map((res) => (
                  <motion.div
                    key={res.id}
                    className={`p-4 rounded-lg flex justify-between items-center transition-all ${
                      res.is_active
                        ? 'bg-blue-500 bg-opacity-20 border border-blue-500'
                        : 'bg-gray-900 bg-opacity-50 border border-gray-700 hover:border-gray-600'
                    }`}
                    whileHover={{ x: 5 }}
                  >
                    <div>
                      <p className="font-semibold text-sm">{res.filename}</p>
                      <p className="text-xs text-gray-400">
                        {new Date(res.created_at).toLocaleDateString()}
                      </p>
                    </div>
                    <div className="flex gap-2">
                      {!res.is_active && (
                        <button
                          onClick={() => selectResume(res.id)}
                          className="px-3 py-1 bg-blue-500 hover:bg-blue-600 rounded text-xs font-semibold transition-colors"
                        >
                          Activate
                        </button>
                      )}
                      <button
                        onClick={() => deleteResume(res.id)}
                        className="px-3 py-1 bg-red-500 hover:bg-red-600 rounded text-xs font-semibold transition-colors"
                      >
                        Delete
                      </button>
                    </div>
                  </motion.div>
                ))}
              </div>
            </CardContent>
          </Card>
        </motion.div>
      )}
    </motion.div>
  )
}
