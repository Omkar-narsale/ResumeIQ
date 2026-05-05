import React, { useState } from 'react'
import { motion } from 'framer-motion'
import { Card, CardTitle, CardContent } from '../components/Card'
import { useApi } from '../hooks/useApi'
import { pageVariants, containerVariants, itemVariants, spinVariants } from '../components/animations'

const targetRoles = [
  'Data Scientist',
  'Machine Learning Engineer',
  'Senior Software Engineer',
  'Cloud Architect',
  'DevOps Engineer',
  'Data Analyst',
]

export const Learning = () => {
  const [targetRole, setTargetRole] = useState(targetRoles[0])
  const [currentSkills, setCurrentSkills] = useState('')
  const [result, setResult] = useState(null)
  const { call, loading, error } = useApi()

  const handleGenerate = async () => {
    if (!currentSkills.trim()) {
      alert('Please enter at least one skill')
      return
    }

    try {
      const skills = currentSkills.split(',').map(s => s.trim()).filter(s => s)
      const data = await call('POST', '/api/roadmap', {
        target_role: targetRole,
        current_skills: skills
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
        <CardTitle>📚 Learning Path Generator</CardTitle>
        <CardContent>
          <div className="space-y-6">
            <div>
              <label className="block text-sm font-semibold mb-3 text-gray-200">Target Role:</label>
              <select
                value={targetRole}
                onChange={(e) => setTargetRole(e.target.value)}
                className="w-full px-4 py-3 rounded-lg bg-gray-800 border border-gray-700 text-gray-300 focus:border-blue-500 focus:outline-none cursor-pointer hover:border-gray-600"
              >
                {targetRoles.map((role) => (
                  <option key={role} value={role}>{role}</option>
                ))}
              </select>
              <p className="text-xs text-gray-400 mt-2">Select the position you want to transition to</p>
            </div>

            <div>
              <label className="block text-sm font-semibold mb-3 text-gray-200">Your Current Skills:</label>
              <input
                type="text"
                value={currentSkills}
                onChange={(e) => setCurrentSkills(e.target.value)}
                placeholder="e.g., Python, SQL, Basic Statistics (comma-separated)"
                className="w-full px-4 py-3 rounded-lg bg-gray-800 border border-gray-700 text-gray-300 placeholder-gray-500 focus:border-blue-500 focus:outline-none"
              />
              <p className="text-xs text-gray-400 mt-2">List your existing technical skills separated by commas</p>
            </div>

            <motion.button
              onClick={handleGenerate}
              disabled={loading || !currentSkills.trim()}
              className={`btn-primary w-full py-3 font-semibold ${!currentSkills.trim() ? 'opacity-50 cursor-not-allowed' : ''}`}
              whileHover={currentSkills.trim() ? { scale: 1.02 } : {}}
              whileTap={currentSkills.trim() ? { scale: 0.98 } : {}}
            >
              {loading ? 'Creating Roadmap...' : 'Generate Learning Roadmap'}
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
        </CardContent>
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
          <Card>
            <CardTitle>🎯 Your Learning Path: {targetRole}</CardTitle>
            <CardContent>
              <p className="text-gray-300 mb-4">Estimated Duration: <span className="text-blue-400 font-semibold">{result.estimated_duration}</span></p>
            </CardContent>
          </Card>

          <motion.div variants={itemVariants}>
            <Card>
              <CardTitle>📖 Learning Phases</CardTitle>
              <CardContent>
                <div className="space-y-6">
                  {result.phases?.map((phase, i) => (
                    <motion.div
                      key={i}
                      className="border-l-4 border-blue-500 pl-5 py-3 hover:bg-gray-800 hover:bg-opacity-50 rounded-r-lg transition-all"
                      initial={{ opacity: 0, x: -20 }}
                      animate={{ opacity: 1, x: 0 }}
                      transition={{ delay: i * 0.1 }}
                    >
                      <div className="flex items-start gap-4">
                        <div className="w-10 h-10 bg-blue-500 rounded-full flex items-center justify-center font-bold text-sm flex-shrink-0 mt-1">
                          {i + 1}
                        </div>
                        <div className="flex-1">
                          <h4 className="text-lg font-semibold text-blue-300 mb-2">
                            {phase.duration}
                          </h4>
                          <p className="text-gray-300 mb-3">
                            {phase.focus}
                          </p>
                          {phase.skills && phase.skills.length > 0 && (
                            <div className="flex flex-wrap gap-2">
                              {phase.skills.map((skill, j) => (
                                <span
                                  key={j}
                                  className="text-xs bg-blue-500 bg-opacity-30 text-blue-300 px-3 py-1 rounded-full border border-blue-400 border-opacity-30"
                                >
                                  {skill}
                                </span>
                              ))}
                            </div>
                          )}
                        </div>
                      </div>
                    </motion.div>
                  ))}
                </div>
              </CardContent>
            </Card>
          </motion.div>

          {result.resources && result.resources.length > 0 && (
            <motion.div variants={itemVariants}>
              <Card>
                <CardTitle>🔗 Recommended Resources</CardTitle>
                <CardContent>
                  <ul className="space-y-3">
                    {result.resources.map((resource, i) => (
                      <li key={i} className="flex gap-3">
                        <span className="text-green-400 font-bold flex-shrink-0">✓</span>
                        <span className="text-gray-300">{resource}</span>
                      </li>
                    ))}
                  </ul>
                </CardContent>
              </Card>
            </motion.div>
          )}

          <motion.div variants={itemVariants} className="flex gap-3">
            <motion.button
              onClick={() => setResult(null)}
              className="btn-secondary"
              whileHover={{ scale: 1.05 }}
              whileTap={{ scale: 0.95 }}
            >
              ← Create Another Roadmap
            </motion.button>
          </motion.div>
        </motion.div>
      )}
    </motion.div>
  )
}
