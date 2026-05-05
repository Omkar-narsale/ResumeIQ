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
  const [questions, setQuestions] = useState(null)
  const [tips, setTips] = useState(null)
  const [currentQuestionIndex, setCurrentQuestionIndex] = useState(0)
  const [answers, setAnswers] = useState({})
  const [feedback, setFeedback] = useState({})
  const [loadingQuestions, setLoadingQuestions] = useState(false)
  const [loadingAnswer, setLoadingAnswer] = useState(false)
  const { call, error } = useApi()

  const handleGenerateQuestions = async () => {
    try {
      setLoadingQuestions(true)
      const data = await call('POST', '/api/interview', {
        role: selectedRole,
        resume: resume.slice(0, 500)
      })
      setQuestions(data.questions)
      setTips(data.tips)
      setAnswers({})
      setFeedback({})
      setCurrentQuestionIndex(0)
      setLoadingQuestions(false)
    } catch (err) {
      setLoadingQuestions(false)
      console.error('Generation failed:', err)
    }
  }

  const handleSubmitAnswer = async () => {
    const answerText = answers[currentQuestionIndex] || ''
    if (!answerText.trim()) {
      alert('Please write an answer before submitting')
      return
    }

    try {
      setLoadingAnswer(true)
      const data = await call('POST', '/api/interview/answer', {
        role: selectedRole,
        question: questions[currentQuestionIndex],
        answer: answerText
      })
      setFeedback(prev => ({
        ...prev,
        [currentQuestionIndex]: data
      }))
      setLoadingAnswer(false)
    } catch (err) {
      setLoadingAnswer(false)
      console.error('Evaluation failed:', err)
    }
  }

  const handleNextQuestion = () => {
    if (currentQuestionIndex < questions.length - 1) {
      setCurrentQuestionIndex(currentQuestionIndex + 1)
    }
  }

  const handlePrevQuestion = () => {
    if (currentQuestionIndex > 0) {
      setCurrentQuestionIndex(currentQuestionIndex - 1)
    }
  }

  return (
    <motion.div
      className="space-y-6"
      variants={pageVariants}
      initial="hidden"
      animate="visible"
    >
      {!questions ? (
        <Card>
          <CardTitle>🎤 Interview Coach</CardTitle>
          <div className="space-y-4">
            <div>
              <label className="block text-sm font-medium mb-2">Target Role:</label>
              <select
                value={selectedRole}
                onChange={(e) => setSelectedRole(e.target.value)}
                className="w-full bg-gray-800 border border-gray-700 rounded px-3 py-2 text-white"
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
                className="w-full h-32 resize-none bg-gray-800 border border-gray-700 rounded px-3 py-2 text-white"
                maxLength={500}
              />
              <p className="text-xs text-gray-400 mt-2">{resume.length}/500 characters</p>
            </div>

            <motion.button
              onClick={handleGenerateQuestions}
              disabled={loadingQuestions}
              className="btn-primary"
              whileHover={{ scale: 1.05 }}
              whileTap={{ scale: 0.95 }}
            >
              {loadingQuestions ? 'Generating...' : 'Generate Questions'}
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
      ) : (
        <motion.div
          className="space-y-6"
          variants={containerVariants}
          initial="hidden"
          animate="visible"
        >
          {/* Progress */}
          <Card>
            <div className="flex justify-between items-center">
              <span className="text-sm text-gray-400">Question {currentQuestionIndex + 1} of {questions.length}</span>
              <span className="text-sm text-blue-400 font-semibold">{selectedRole}</span>
            </div>
            <div className="w-full bg-gray-700 rounded-full h-2 mt-2">
              <div
                className="bg-blue-500 h-2 rounded-full transition-all"
                style={{ width: `${((currentQuestionIndex + 1) / questions.length) * 100}%` }}
              />
            </div>
          </Card>

          {/* Question */}
          <motion.div variants={itemVariants}>
            <Card>
              <CardTitle>❓ Question</CardTitle>
              <CardContent>
                <p className="text-lg text-blue-300 mb-4">{questions[currentQuestionIndex]}</p>
              </CardContent>
            </Card>
          </motion.div>

          {/* Answer Input */}
          <motion.div variants={itemVariants}>
            <Card>
              <CardTitle>💬 Your Answer</CardTitle>
              <CardContent>
                <textarea
                  value={answers[currentQuestionIndex] || ''}
                  onChange={(e) => setAnswers({
                    ...answers,
                    [currentQuestionIndex]: e.target.value.slice(0, 1000)
                  })}
                  placeholder="Write your answer here..."
                  className="w-full h-40 resize-none bg-gray-800 border border-gray-700 rounded px-3 py-2 text-white"
                  maxLength={1000}
                />
                <p className="text-xs text-gray-400 mt-2">{(answers[currentQuestionIndex] || '').length}/1000 characters</p>
              </CardContent>
            </Card>
          </motion.div>

          {/* Feedback */}
          {feedback[currentQuestionIndex] && (
            <motion.div variants={itemVariants}>
              <Card className="border-l-4 border-green-500">
                <CardTitle>✅ Feedback</CardTitle>
                <CardContent className="space-y-4">
                  <div>
                    <div className="flex items-center gap-2 mb-2">
                      <span className="text-sm font-medium">Score:</span>
                      <span className="text-2xl font-bold text-green-400">{feedback[currentQuestionIndex].score}/10</span>
                    </div>
                  </div>
                  <div>
                    <p className="text-sm font-medium mb-2">Feedback:</p>
                    <p className="text-sm text-gray-300">{feedback[currentQuestionIndex].feedback}</p>
                  </div>
                  <div>
                    <p className="text-sm font-medium mb-2">💡 Better Answer Example:</p>
                    <p className="text-sm text-gray-300 italic">{feedback[currentQuestionIndex].better_answer}</p>
                  </div>
                </CardContent>
              </Card>
            </motion.div>
          )}

          {/* Tips */}
          <motion.div variants={itemVariants}>
            <Card>
              <CardTitle>💡 Interview Tips</CardTitle>
              <CardContent>
                <ul className="space-y-3">
                  {tips.map((tip, i) => (
                    <li key={i} className="flex gap-3">
                      <span className="text-yellow-400 font-bold">•</span>
                      <span className="text-sm">{tip}</span>
                    </li>
                  ))}
                </ul>
              </CardContent>
            </Card>
          </motion.div>

          {/* Action Buttons */}
          <motion.div variants={itemVariants} className="flex gap-4">
            <motion.button
              onClick={handlePrevQuestion}
              disabled={currentQuestionIndex === 0}
              className="btn-primary flex-1 disabled:opacity-50 disabled:cursor-not-allowed"
              whileHover={{ scale: 1.05 }}
              whileTap={{ scale: 0.95 }}
            >
              ← Previous
            </motion.button>

            <motion.button
              onClick={handleSubmitAnswer}
              disabled={loadingAnswer || !answers[currentQuestionIndex]?.trim()}
              className="btn-primary flex-1 disabled:opacity-50 disabled:cursor-not-allowed"
              whileHover={{ scale: 1.05 }}
              whileTap={{ scale: 0.95 }}
            >
              {loadingAnswer ? 'Evaluating...' : '✓ Submit Answer'}
            </motion.button>

            <motion.button
              onClick={handleNextQuestion}
              disabled={currentQuestionIndex === questions.length - 1}
              className="btn-primary flex-1 disabled:opacity-50 disabled:cursor-not-allowed"
              whileHover={{ scale: 1.05 }}
              whileTap={{ scale: 0.95 }}
            >
              Next →
            </motion.button>
          </motion.div>

          {/* Reset */}
          <motion.button
            onClick={() => {
              setQuestions(null)
              setResume('')
            }}
            className="w-full text-gray-400 hover:text-gray-300 text-sm py-2"
            whileHover={{ scale: 1.02 }}
          >
            Start New Session
          </motion.button>
        </motion.div>
      )}
    </motion.div>
  )
}
