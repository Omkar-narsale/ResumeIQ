import React, { useState, useEffect } from 'react'
import { motion } from 'framer-motion'
import { Card, CardTitle, CardContent } from '../components/Card'
import { useApi } from '../hooks/useApi'
import { pageVariants, containerVariants, itemVariants, spinVariants } from '../components/animations'

export const Mentorship = () => {
  const [currentSkills, setCurrentSkills] = useState('')
  const [goal, setGoal] = useState('')
  const [experience, setExperience] = useState(0)
  const [mentorMatch, setMentorMatch] = useState(null)
  const [mentors, setMentors] = useState(null)
  const [loading, setLoading] = useState(false)
  const { call, error } = useApi()

  const handleFindMentors = async () => {
    if (!currentSkills.trim() || !goal.trim()) {
      alert('Please fill in all fields')
      return
    }

    setLoading(true)
    try {
      const skillsArray = currentSkills.split(',').map(s => s.trim()).filter(s => s)
      const matchData = await call('POST', '/api/mentor/match', {
        current_skills: skillsArray,
        goal: goal,
        experience_years: experience
      })
      setMentorMatch(matchData)

      const mentorsData = await call('GET', '/api/mentors/available', null)
      setMentors(mentorsData)
    } catch (err) {
      console.error('Failed to find mentors:', err)
    } finally {
      setLoading(false)
    }
  }

  const handleRequestMentor = async (mentorId) => {
    try {
      await call('POST', `/api/mentor/request/${mentorId}`, {
        goal: goal
      })
      alert('Mentorship request sent successfully!')
    } catch (err) {
      console.error('Request failed:', err)
      alert('Failed to send mentorship request')
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
        <CardTitle>👥 Mentorship Matching</CardTitle>
        <p className="text-gray-400 text-sm mb-4">Find experienced mentors to guide your career growth</p>
      </Card>

      <motion.div
        className="grid grid-cols-1 md:grid-cols-2 gap-6"
        variants={containerVariants}
        initial="hidden"
        animate="visible"
      >
        <motion.div variants={itemVariants}>
          <Card>
            <CardTitle>🎯 Your Profile</CardTitle>
            <CardContent>
              <div className="space-y-4">
                <div>
                  <label className="block text-sm font-medium mb-2">Current Skills (comma-separated):</label>
                  <input
                    type="text"
                    value={currentSkills}
                    onChange={(e) => setCurrentSkills(e.target.value)}
                    placeholder="e.g., Python, React, Leadership"
                    className="w-full px-3 py-2 rounded border border-gray-600 bg-gray-800"
                  />
                </div>

                <div>
                  <label className="block text-sm font-medium mb-2">Career Goal:</label>
                  <input
                    type="text"
                    value={goal}
                    onChange={(e) => setGoal(e.target.value)}
                    placeholder="e.g., Senior Engineer, Team Lead"
                    className="w-full px-3 py-2 rounded border border-gray-600 bg-gray-800"
                  />
                </div>

                <div>
                  <label className="block text-sm font-medium mb-2">Years of Experience:</label>
                  <input
                    type="number"
                    value={experience}
                    onChange={(e) => setExperience(parseInt(e.target.value))}
                    min="0"
                    className="w-full px-3 py-2 rounded border border-gray-600 bg-gray-800"
                  />
                </div>

                <motion.button
                  onClick={handleFindMentors}
                  disabled={loading}
                  className="w-full btn-primary"
                  whileHover={{ scale: 1.05 }}
                  whileTap={{ scale: 0.95 }}
                >
                  {loading ? 'Finding Mentors...' : 'Find Mentors'}
                </motion.button>
              </div>
            </CardContent>
          </Card>
        </motion.div>

        {mentorMatch && (
          <motion.div variants={itemVariants}>
            <Card>
              <CardTitle>🎓 Recommended Expertise</CardTitle>
              <CardContent>
                <div className="space-y-4">
                  <div>
                    <p className="text-sm text-gray-400 mb-2">Ideal Mentor Should Have:</p>
                    <ul className="space-y-2">
                      {mentorMatch.ideal_mentor_traits.map((trait, i) => (
                        <li key={i} className="flex gap-2 text-sm">
                          <span className="text-green-400">✓</span>
                          <span>{trait}</span>
                        </li>
                      ))}
                    </ul>
                  </div>

                  <div className="border-t border-gray-700 pt-4">
                    <p className="text-sm text-gray-400">Focus Area:</p>
                    <p className="text-yellow-300 font-semibold mt-1">
                      {mentorMatch.mentorship_focus}
                    </p>
                  </div>

                  <div className="bg-blue-500 bg-opacity-20 border border-blue-500 p-3 rounded-lg">
                    <p className="text-sm text-blue-300">
                      💡 You'll benefit most from mentors with expertise in: <strong>{mentorMatch.recommended_expertise.join(', ')}</strong>
                    </p>
                  </div>
                </div>
              </CardContent>
            </Card>
          </motion.div>
        )}
      </motion.div>

      {loading && (
        <motion.div className="flex justify-center py-8" variants={spinVariants}>
          <motion.div
            className="w-12 h-12 border-4 border-blue-500 border-t-transparent rounded-full"
            animate="rotate"
          />
        </motion.div>
      )}

      {mentors && mentors.mentors && mentors.mentors.length > 0 && (
        <motion.div variants={itemVariants}>
          <Card>
            <CardTitle>🌟 Available Mentors ({mentors.total_mentors})</CardTitle>
            <CardContent>
              <div className="space-y-4">
                {mentors.mentors.map((mentor, idx) => (
                  <motion.div
                    key={mentor.id}
                    className="border border-gray-700 rounded-lg p-4 hover:border-blue-500 transition-colors"
                    whileHover={{ scale: 1.02 }}
                  >
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                      <div>
                        <div className="flex items-center gap-2 mb-2">
                          <span className="text-2xl">👨‍💼</span>
                          <div>
                            <p className="font-semibold">Mentor #{mentor.id}</p>
                            <p className="text-xs text-gray-400">{mentor.expertise}</p>
                          </div>
                        </div>

                        <ul className="text-sm text-gray-300 space-y-1">
                          <li>⏱️ {mentor.years_experience}+ years experience</li>
                          <li>⭐ Rating: {mentor.rating}/5</li>
                          <li>👥 {mentor.total_mentees} active mentees</li>
                          <li>
                            💰 {mentor.hourly_rate === 0 ? 'Free' : `$${mentor.hourly_rate}/hr`}
                          </li>
                        </ul>
                      </div>

                      <div className="flex flex-col justify-between">
                        <div>
                          <p className="text-sm font-semibold text-gray-300">Availability:</p>
                          <p className="text-sm text-green-400">{mentor.availability}</p>
                        </div>

                        <motion.button
                          onClick={() => handleRequestMentor(mentor.id)}
                          className="px-4 py-2 bg-blue-500 hover:bg-blue-600 rounded font-semibold text-sm"
                          whileHover={{ scale: 1.05 }}
                          whileTap={{ scale: 0.95 }}
                        >
                          Connect Now
                        </motion.button>
                      </div>
                    </div>
                  </motion.div>
                ))}
              </div>
            </CardContent>
          </Card>
        </motion.div>
      )}

      <motion.div variants={itemVariants}>
        <Card>
          <CardTitle>❓ About Mentorship</CardTitle>
          <CardContent>
            <div className="space-y-4 text-sm">
              <div>
                <p className="font-semibold text-blue-300 mb-2">What is Mentorship?</p>
                <p className="text-gray-300">
                  Connect with experienced professionals who can guide you through career transitions, skill development, and strategic planning.
                </p>
              </div>

              <div>
                <p className="font-semibold text-green-300 mb-2">Benefits:</p>
                <ul className="text-gray-300 space-y-1">
                  <li>✓ Personalized career guidance</li>
                  <li>✓ Industry insights and trends</li>
                  <li>✓ Networking opportunities</li>
                  <li>✓ Resume and interview preparation</li>
                  <li>✓ Skill development roadmap</li>
                </ul>
              </div>

              <div>
                <p className="font-semibold text-purple-300 mb-2">Getting Started:</p>
                <ol className="text-gray-300 space-y-1 list-decimal list-inside">
                  <li>Fill in your profile and career goals</li>
                  <li>Browse available mentors</li>
                  <li>Send a connection request</li>
                  <li>Start your mentoring journey!</li>
                </ol>
              </div>
            </div>
          </CardContent>
        </Card>
      </motion.div>

      {error && (
        <motion.div
          className="bg-red-500 bg-opacity-20 border border-red-500 text-red-300 p-3 rounded-lg"
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
        >
          {error}
        </motion.div>
      )}
    </motion.div>
  )
}
