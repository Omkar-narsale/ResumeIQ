import React, { useState, useEffect } from 'react'
import { motion } from 'framer-motion'
import { Card, CardTitle, CardContent } from '../components/Card'
import { useApi } from '../hooks/useApi'
import { pageVariants, containerVariants, itemVariants } from '../components/animations'

export const ResumeVersioning = () => {
  const [resumes, setResumes] = useState([])
  const [currentResume, setCurrentResume] = useState(null)
  const [versionName, setVersionName] = useState('')
  const [description, setDescription] = useState('')
  const { call, loading, error } = useApi()

  useEffect(() => {
    loadResumes()
  }, [])

  const loadResumes = async () => {
    try {
      const data = await call('GET', '/api/resumes', null)
      setResumes(data)

      const current = await call('GET', '/api/current-resume', null)
      if (current) setCurrentResume(current)
    } catch (err) {
      console.error('Failed to load resumes:', err)
    }
  }

  const handleSelectResume = async (resumeId) => {
    try {
      await call('POST', `/api/resumes/${resumeId}/select`, {})
      loadResumes()
    } catch (err) {
      console.error('Failed to select resume:', err)
    }
  }

  const handleDeleteResume = async (resumeId) => {
    if (window.confirm('Delete this resume version?')) {
      try {
        await call('DELETE', `/api/resumes/${resumeId}`, null)
        loadResumes()
      } catch (err) {
        console.error('Failed to delete resume:', err)
      }
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
        <CardTitle>📌 Resume Versions</CardTitle>
        <p className="text-gray-400 text-sm mb-4">Manage and organize multiple versions of your resume</p>
      </Card>

      {error && (
        <motion.div
          className="bg-red-500 bg-opacity-20 border border-red-500 text-red-300 p-3 rounded-lg"
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
        >
          {error}
        </motion.div>
      )}

      {resumes.length > 0 ? (
        <motion.div
          className="grid grid-cols-1 md:grid-cols-2 gap-6"
          variants={containerVariants}
          initial="hidden"
          animate="visible"
        >
          {resumes.map((resume, index) => (
            <motion.div key={resume.id} variants={itemVariants}>
              <Card>
                <div className="flex justify-between items-start mb-3">
                  <CardTitle className="text-lg">📄 {resume.filename}</CardTitle>
                  {resume.is_active && (
                    <span className="bg-green-500 bg-opacity-20 text-green-300 px-2 py-1 rounded text-xs">
                      Active
                    </span>
                  )}
                </div>
                <CardContent>
                  <div className="space-y-3 text-sm">
                    <div>
                      <p className="text-gray-400">Created:</p>
                      <p className="text-gray-300">{new Date(resume.created_at).toLocaleDateString()}</p>
                    </div>
                    <div className="flex gap-2 pt-2">
                      {!resume.is_active && (
                        <motion.button
                          onClick={() => handleSelectResume(resume.id)}
                          disabled={loading}
                          className="flex-1 px-3 py-2 bg-blue-500 hover:bg-blue-600 rounded text-sm transition-colors"
                          whileHover={{ scale: 1.05 }}
                          whileTap={{ scale: 0.95 }}
                        >
                          Select
                        </motion.button>
                      )}
                      <motion.button
                        onClick={() => handleDeleteResume(resume.id)}
                        disabled={loading}
                        className="flex-1 px-3 py-2 bg-red-500 hover:bg-red-600 rounded text-sm transition-colors"
                        whileHover={{ scale: 1.05 }}
                        whileTap={{ scale: 0.95 }}
                      >
                        Delete
                      </motion.button>
                    </div>
                  </div>
                </CardContent>
              </Card>
            </motion.div>
          ))}
        </motion.div>
      ) : (
        <Card>
          <CardContent>
            <p className="text-gray-400 text-center py-8">No resumes uploaded yet. Upload one to get started!</p>
          </CardContent>
        </Card>
      )}

      {currentResume && (
        <motion.div variants={itemVariants}>
          <Card>
            <CardTitle>📋 Current Active Resume</CardTitle>
            <CardContent>
              <div className="space-y-3">
                <div>
                  <p className="text-gray-400 text-sm">Filename:</p>
                  <p className="text-lg font-semibold text-blue-400">{currentResume.filename}</p>
                </div>
                <div>
                  <p className="text-gray-400 text-sm">Preview:</p>
                  <div className="bg-gray-800 p-3 rounded mt-2 max-h-40 overflow-auto text-sm text-gray-300">
                    {currentResume.extracted_text?.substring(0, 300)}...
                  </div>
                </div>
              </div>
            </CardContent>
          </Card>
        </motion.div>
      )}

      <Card>
        <CardTitle>📂 Quick Info</CardTitle>
        <CardContent>
          <div className="grid grid-cols-2 gap-4">
            <div>
              <p className="text-gray-400 text-sm">Total Versions:</p>
              <p className="text-3xl font-bold text-blue-400">{resumes.length}</p>
            </div>
            <div>
              <p className="text-gray-400 text-sm">Active:</p>
              <p className="text-3xl font-bold text-green-400">1</p>
            </div>
          </div>
        </CardContent>
      </Card>

      <Card>
        <CardTitle>💡 Tips for Resume Versioning</CardTitle>
        <CardContent>
          <ul className="space-y-2 text-sm text-gray-300">
            <li>✓ Create versions for different job types (Tech, Startup, Enterprise)</li>
            <li>✓ Keep an updated master version</li>
            <li>✓ Use keywords from job descriptions in targeted versions</li>
            <li>✓ Compare versions side-by-side to find the strongest one</li>
          </ul>
        </CardContent>
      </Card>
    </motion.div>
  )
}
