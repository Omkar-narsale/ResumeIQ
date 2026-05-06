import React, { useState } from 'react'
import { motion } from 'framer-motion'
import { Card, CardTitle, CardContent } from '../components/Card'
import { useApi } from '../hooks/useApi'
import { pageVariants, containerVariants, itemVariants, spinVariants } from '../components/animations'

export const BatchJobMatch = () => {
  const [resume, setResume] = useState('')
  const [jobDescriptions, setJobDescriptions] = useState('')
  const [result, setResult] = useState(null)
  const { call, loading, error } = useApi()

  const handleMatch = async () => {
    if (!resume.trim() || !jobDescriptions.trim()) {
      alert('Please fill in both fields')
      return
    }

    // Split job descriptions by separator (e.g., "---" or "Job 1:" pattern)
    const jobs = jobDescriptions
      .split(/(?:---|Job\s*\d+:|Position\s*\d+:)/i)
      .map(j => j.trim())
      .filter(j => j.length > 20)

    if (jobs.length === 0) {
      alert('Could not parse job descriptions. Try separating with "---"')
      return
    }

    try {
      const data = await call('POST', '/api/batch-match-jobs', {
        resume: resume.slice(0, 2000),
        job_descriptions: jobs.slice(0, 10)
      })
      setResult(data)
    } catch (err) {
      console.error('Batch matching failed:', err)
    }
  }

  const getScoreColor = (score) => {
    if (score >= 8) return 'text-green-400'
    if (score >= 6) return 'text-yellow-400'
    if (score >= 4) return 'text-orange-400'
    return 'text-red-400'
  }

  const getFitBadgeColor = (fit) => {
    switch (fit) {
      case 'Excellent':
        return 'bg-green-500 bg-opacity-20 text-green-300'
      case 'Good':
        return 'bg-yellow-500 bg-opacity-20 text-yellow-300'
      case 'Fair':
        return 'bg-orange-500 bg-opacity-20 text-orange-300'
      default:
        return 'bg-red-500 bg-opacity-20 text-red-300'
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
        <CardTitle>🔍 Batch Job Matching</CardTitle>
        <p className="text-gray-400 text-sm mb-4">Compare your resume against multiple job descriptions at once. Separate jobs with "---"</p>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div>
            <label className="block text-sm font-medium mb-2">Your Resume:</label>
            <textarea
              value={resume}
              onChange={(e) => setResume(e.target.value.slice(0, 2000))}
              placeholder="Paste your resume..."
              className="w-full h-40 resize-none"
              maxLength={2000}
            />
            <p className="text-xs text-gray-400 mt-2">{resume.length}/2000 characters</p>
          </div>

          <div>
            <label className="block text-sm font-medium mb-2">Job Descriptions (separate with ---):</label>
            <textarea
              value={jobDescriptions}
              onChange={(e) => setJobDescriptions(e.target.value)}
              placeholder="Paste multiple job descriptions, separated by ---"
              className="w-full h-40 resize-none"
            />
            <p className="text-xs text-gray-400 mt-2">Max 10 jobs</p>
          </div>
        </div>

        <motion.button
          onClick={handleMatch}
          disabled={loading}
          className="btn-primary mt-4"
          whileHover={{ scale: 1.05 }}
          whileTap={{ scale: 0.95 }}
        >
          {loading ? 'Analyzing...' : 'Analyze All Jobs'}
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
              <CardTitle>📊 Summary</CardTitle>
              <CardContent>
                <div className="grid grid-cols-3 gap-4">
                  <div>
                    <p className="text-gray-400 text-sm">Jobs Analyzed</p>
                    <p className="text-3xl font-bold text-blue-400">{result.total_jobs}</p>
                  </div>
                  <div>
                    <p className="text-gray-400 text-sm">Average Score</p>
                    <p className="text-3xl font-bold text-green-400">{result.avg_score}/10</p>
                  </div>
                  <div>
                    <p className="text-gray-400 text-sm">Best Match</p>
                    <p className="text-3xl font-bold text-purple-400">
                      {result.best_matches[0]?.match_score || 'N/A'}
                    </p>
                  </div>
                </div>
              </CardContent>
            </Card>
          </motion.div>

          {result.best_matches && result.best_matches.length > 0 && (
            <motion.div variants={itemVariants}>
              <Card>
                <CardTitle>🏆 Top Matches (Best 3)</CardTitle>
                <CardContent>
                  <div className="space-y-4">
                    {result.best_matches.map((match, idx) => (
                      <div key={idx} className="border-b border-gray-700 pb-4 last:border-b-0">
                        <div className="flex justify-between items-start mb-2">
                          <div>
                            <p className="font-semibold text-lg">Job #{match.job_index}</p>
                            <p className="text-sm text-gray-400">Match: {match.match_percentage}%</p>
                          </div>
                          <span className={`px-3 py-1 rounded-full text-sm font-semibold ${getFitBadgeColor(match.fit_level)}`}>
                            {match.fit_level}
                          </span>
                        </div>

                        <div className="flex items-center gap-2 mb-3">
                          <div className="text-4xl font-bold">{match.match_score}</div>
                          <div className="flex-1 bg-gray-700 h-2 rounded-full overflow-hidden">
                            <motion.div
                              className="bg-green-500 h-full"
                              initial={{ width: 0 }}
                              animate={{ width: `${(match.match_score / 10) * 100}%` }}
                              transition={{ duration: 0.6 }}
                            />
                          </div>
                        </div>

                        <div className="grid grid-cols-2 gap-3 text-sm">
                          <div>
                            <p className="text-green-400">Matched Skills:</p>
                            <div className="flex flex-wrap gap-1 mt-1">
                              {match.skills_matched.map((s, i) => (
                                <span key={i} className="bg-green-500 bg-opacity-20 text-green-300 px-2 py-1 rounded text-xs">
                                  {s}
                                </span>
                              ))}
                            </div>
                          </div>
                          <div>
                            <p className="text-red-400">Missing Skills:</p>
                            <div className="flex flex-wrap gap-1 mt-1">
                              {match.skills_missing.map((s, i) => (
                                <span key={i} className="bg-red-500 bg-opacity-20 text-red-300 px-2 py-1 rounded text-xs">
                                  {s}
                                </span>
                              ))}
                            </div>
                          </div>
                        </div>
                      </div>
                    ))}
                  </div>
                </CardContent>
              </Card>
            </motion.div>
          )}

          {result.all_results && result.all_results.length > 3 && (
            <motion.div variants={itemVariants}>
              <Card>
                <CardTitle>📋 All Results (Ranked)</CardTitle>
                <CardContent>
                  <div className="overflow-x-auto">
                    <table className="w-full text-sm">
                      <thead>
                        <tr className="border-b border-gray-700">
                          <th className="text-left py-2">Job</th>
                          <th className="text-center py-2">Score</th>
                          <th className="text-center py-2">Match %</th>
                          <th className="text-left py-2">Fit</th>
                        </tr>
                      </thead>
                      <tbody>
                        {result.all_results.map((match, idx) => (
                          <tr key={idx} className="border-b border-gray-800 hover:bg-gray-800 bg-opacity-30">
                            <td className="py-2">#{match.job_index}</td>
                            <td className={`text-center font-bold ${getScoreColor(match.match_score)}`}>
                              {match.match_score}
                            </td>
                            <td className="text-center">{match.match_percentage}%</td>
                            <td>
                              <span className={`px-2 py-1 rounded text-xs ${getFitBadgeColor(match.fit_level)}`}>
                                {match.fit_level}
                              </span>
                            </td>
                          </tr>
                        ))}
                      </tbody>
                    </table>
                  </div>
                </CardContent>
              </Card>
            </motion.div>
          )}

          <motion.div variants={itemVariants}>
            <Card>
              <CardTitle>💡 Tips for Better Matches</CardTitle>
              <CardContent>
                <ul className="space-y-2 text-sm text-gray-300">
                  <li>✓ Focus on top 3 matches first</li>
                  <li>✓ Learn missing skills for high-priority jobs</li>
                  <li>✓ Customize resume for each top match</li>
                  <li>✓ Highlight common skills across all jobs</li>
                </ul>
              </CardContent>
            </Card>
          </motion.div>
        </motion.div>
      )}
    </motion.div>
  )
}
