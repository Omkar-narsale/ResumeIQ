import React, { useState } from 'react'
import { motion } from 'framer-motion'
import { Card, CardTitle, CardContent } from '../components/Card'
import { useApi } from '../hooks/useApi'
import { pageVariants, containerVariants, itemVariants, spinVariants } from '../components/animations'

export const SkillGapAnalyzer = () => {
  const [currentSkills, setCurrentSkills] = useState('')
  const [targetRole, setTargetRole] = useState('')
  const [result, setResult] = useState(null)
  const { call, loading, error } = useApi()

  const handleAnalyze = async () => {
    if (!currentSkills.trim() || !targetRole.trim()) {
      alert('Please fill in both fields')
      return
    }

    const skillsArray = currentSkills.split(',').map(s => s.trim()).filter(s => s)

    try {
      const data = await call('POST', '/api/skill-gaps', {
        current_skills: skillsArray,
        target_role: targetRole
      })
      setResult(data)
    } catch (err) {
      console.error('Analysis failed:', err)
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
        <CardTitle>🎓 Skill Gap Analyzer</CardTitle>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div>
            <label className="block text-sm font-medium mb-2">Current Skills (comma-separated):</label>
            <textarea
              value={currentSkills}
              onChange={(e) => setCurrentSkills(e.target.value)}
              placeholder="e.g., Python, React, SQL, Node.js"
              className="w-full h-24 resize-none"
            />
          </div>

          <div>
            <label className="block text-sm font-medium mb-2">Target Role:</label>
            <input
              type="text"
              value={targetRole}
              onChange={(e) => setTargetRole(e.target.value)}
              placeholder="e.g., Data Scientist, Senior Engineer"
              className="w-full h-10 px-3 py-2 rounded border border-gray-600 bg-gray-800"
            />
          </div>
        </div>

        <motion.button
          onClick={handleAnalyze}
          disabled={loading}
          className="btn-primary mt-4"
          whileHover={{ scale: 1.05 }}
          whileTap={{ scale: 0.95 }}
        >
          {loading ? 'Analyzing...' : 'Analyze Gaps'}
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
              <CardTitle>📊 Coverage</CardTitle>
              <div className="text-center py-6">
                <motion.div
                  className="text-6xl font-bold text-blue-400 mb-4"
                  initial={{ scale: 0 }}
                  animate={{ scale: 1 }}
                  transition={{ delay: 0.3, type: 'spring' }}
                >
                  {result.coverage_percentage}%
                </motion.div>
                <div className="w-full bg-gray-700 h-3 rounded-full overflow-hidden">
                  <motion.div
                    className="bg-gradient-to-r from-blue-500 to-blue-400 h-full"
                    initial={{ width: 0 }}
                    animate={{ width: `${result.coverage_percentage}%` }}
                    transition={{ duration: 1 }}
                  />
                </div>
                <p className="text-gray-400 text-sm mt-3">Skills you already have</p>
              </div>
            </Card>
          </motion.div>

          <motion.div variants={itemVariants}>
            <Card>
              <CardTitle>⏱️ Learning Timeline</CardTitle>
              <CardContent>
                <div className="text-2xl font-bold text-yellow-400">
                  {result.estimated_learning_time}
                </div>
                <p className="text-gray-400 text-sm mt-2">Estimated time to learn new skills</p>
              </CardContent>
            </Card>
          </motion.div>

          <motion.div variants={itemVariants} className="md:col-span-2">
            <Card>
              <CardTitle>✅ Skills You Already Have</CardTitle>
              <CardContent>
                <div className="flex flex-wrap gap-2">
                  {result.mastered_skills?.map((s, i) => (
                    <span key={i} className="bg-green-500 bg-opacity-20 text-green-300 px-3 py-1 rounded-full text-sm">
                      ✓ {s}
                    </span>
                  ))}
                </div>
              </CardContent>
            </Card>
          </motion.div>

          <motion.div variants={itemVariants} className="md:col-span-2">
            <Card>
              <CardTitle>🎯 Learning Priority ({result.gap_count} gaps)</CardTitle>
              <CardContent>
                <div className="space-y-2">
                  {result.learning_priority?.map((s, i) => (
                    <div key={i} className="flex items-center gap-3">
                      <span className="bg-red-500 bg-opacity-30 text-red-300 px-2 py-1 rounded text-xs font-bold">
                        {i + 1}
                      </span>
                      <span className="text-red-300">{s}</span>
                    </div>
                  ))}
                </div>
              </CardContent>
            </Card>
          </motion.div>

          {result.gaps?.length > 0 && (
            <motion.div variants={itemVariants} className="md:col-span-2">
              <Card>
                <CardTitle>📚 All Skills to Learn</CardTitle>
                <CardContent>
                  <div className="flex flex-wrap gap-2">
                    {result.gaps?.map((s, i) => (
                      <span key={i} className="bg-red-500 bg-opacity-20 text-red-300 px-3 py-1 rounded-full text-sm">
                        + {s}
                      </span>
                    ))}
                  </div>
                </CardContent>
              </Card>
            </motion.div>
          )}

          {result.additional_skills?.length > 0 && (
            <motion.div variants={itemVariants} className="md:col-span-2">
              <Card>
                <CardTitle>⭐ Bonus Skills (Additional)</CardTitle>
                <CardContent>
                  <div className="flex flex-wrap gap-2">
                    {result.additional_skills?.map((s, i) => (
                      <span key={i} className="bg-purple-500 bg-opacity-20 text-purple-300 px-3 py-1 rounded-full text-sm">
                        ★ {s}
                      </span>
                    ))}
                  </div>
                </CardContent>
              </Card>
            </motion.div>
          )}
        </motion.div>
      )}
    </motion.div>
  )
}
