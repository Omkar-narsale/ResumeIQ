import React, { useState } from 'react'
import { motion } from 'framer-motion'
import { Card, CardTitle, CardContent } from '../components/Card'
import { useApi } from '../hooks/useApi'
import { pageVariants, containerVariants, itemVariants, spinVariants } from '../components/animations'

const roles = [
  'Software Engineer',
  'Senior Software Engineer',
  'Frontend Developer',
  'Backend Developer',
  'Data Scientist',
  'ML Engineer',
  'DevOps Engineer',
  'Product Manager',
]

export const Interview = () => {
  const [selectedRole, setSelectedRole] = useState(roles[0])
  const [resume, setResume] = useState('')
  const [result, setResult] = useState(null)
  const { call, loading, error } = useApi()

  const handleGenerate = async () => {
    try {
      const data = await call('POST', '/api/interview', {
        role: selectedRole,
        resume: resume.slice(0, 500)
      })
      setResult(data)
    } catch (err) {
      console.error('Generation failed:', err)
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
        <CardTitle>🎤 Interview Coach</CardTitle>
        <div className="space-y-4">
          <div>
            <label className="block text-sm font-medium mb-2">Target Role:</label>
            <select
              value={selectedRole}
              onChange={(e) => setSelectedRole(e.target.value)}
              className="w-full"
            >
              {roles.map((role) => (
                <option key={role} value={role}>{role}</option>
              ))}
            </select>
          </div>

          <div>
            <label className="block text-sm font-medium mb-2">Your Resume (Optional):</label>
            <textarea
              value={resume}
              onChange={(e) => setResume(e.target.value.slice(0, 500))}
              placeholder="Paste your resume for role-specific questions..."
              className="w-full h-32 resize-none"
              maxLength={500}
            />
            <p className="text-xs text-gray-400 mt-2">{resume.length}/500 characters</p>
          </div>

          <motion.button
            onClick={handleGenerate}
            disabled={loading}
            className="btn-primary"
            whileHover={{ scale: 1.05 }}
            whileTap={{ scale: 0.95 }}
          >
            {loading ? 'Generating...' : 'Generate Questions'}
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
          className="space-y-6"
          variants={containerVariants}
          initial="hidden"
          animate="visible"
        >
          <Card>
            <CardTitle>❓ Interview Questions</CardTitle>
            <CardContent>
              <div className="space-y-4">
                {result.questions?.map((q, i) => (
                  <motion.div
                    key={i}
                    className="bg-gray-800 p-4 rounded-lg"
                    initial={{ opacity: 0, x: -20 }}
                    animate={{ opacity: 1, x: 0 }}
                    transition={{ delay: i * 0.1 }}
                  >
                    <p className="font-semibold text-blue-400 mb-2">Q{i + 1}: {q}</p>
                    <textarea
                      placeholder="Write your answer here..."
                      className="w-full h-24"
                    />
                  </motion.div>
                ))}
              </div>
            </CardContent>
          </Card>

          <motion.div variants={itemVariants}>
            <Card>
              <CardTitle>💡 Interview Tips</CardTitle>
              <CardContent>
                <ul className="space-y-3">
                  {result.tips?.map((tip, i) => (
                    <li key={i} className="flex gap-3">
                      <span className="text-yellow-400 font-bold">•</span>
                      <span>{tip}</span>
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
