import React from 'react'
import { motion } from 'framer-motion'

export const SuggestedPrompts = ({ mode, onSelectPrompt }) => {
  const prompts = {
    resume_expert: [
      'How can I improve my resume for [role]?',
      'What changes will boost my ATS score?',
      'Which bullet point is strongest?',
      'Suggest a professional summary'
    ],
    career_mentor: [
      'What skills should I prioritize learning?',
      'How do I transition to [target role]?',
      'What projects would strengthen my profile?',
      'What are the top skills for my career path?'
    ],
    interview_coach: [
      'Generate 5 interview questions for me',
      'How do I answer behavioral questions?',
      'Can we do a mock interview?',
      'Teach me the STAR method with an example'
    ]
  }

  const modePrompts = prompts[mode] || prompts.career_mentor

  return (
    <motion.div
      className="flex flex-wrap gap-2"
      initial={{ opacity: 0, y: -10 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.2 }}
    >
      {modePrompts.map((prompt, idx) => (
        <motion.button
          key={idx}
          onClick={() => onSelectPrompt(prompt)}
          className="px-3 py-1.5 bg-gray-800 border border-gray-700 text-gray-300 text-xs rounded-full hover:border-blue-500 hover:text-blue-400 hover:bg-blue-500/10 transition-all"
          whileHover={{ scale: 1.05, y: -2 }}
          whileTap={{ scale: 0.95 }}
        >
          ✨ {prompt}
        </motion.button>
      ))}
    </motion.div>
  )
}
