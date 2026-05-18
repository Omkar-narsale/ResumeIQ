import React, { useState } from 'react'
import { motion, AnimatePresence } from 'framer-motion'

export const ModeSelector = ({ activeMode, onModeChange, onClearMode }) => {
  const [showConfirm, setShowConfirm] = useState(null)

  const modes = [
    {
      id: 'resume_expert',
      label: 'Resume Expert',
      icon: '📄',
      description: 'Get specific resume feedback & optimization tips',
      color: 'from-blue-500 to-blue-600'
    },
    {
      id: 'career_mentor',
      label: 'Career Mentor',
      icon: '🎯',
      description: 'Strategic career guidance & skill development',
      color: 'from-purple-500 to-purple-600'
    },
    {
      id: 'interview_coach',
      label: 'Interview Coach',
      icon: '⭐',
      description: 'Interview prep & behavioral questions',
      color: 'from-green-500 to-green-600'
    }
  ]

  const handleModeChange = (newMode) => {
    if (activeMode !== newMode) {
      setShowConfirm(newMode)
    }
  }

  const confirmModeChange = (newMode) => {
    onClearMode(activeMode)
    onModeChange(newMode)
    setShowConfirm(null)
  }

  return (
    <div className="space-y-4">
      <div className="space-y-2">
        {modes.map((mode) => (
          <motion.button
            key={mode.id}
            onClick={() => handleModeChange(mode.id)}
            className={`w-full text-left p-4 rounded-lg border-2 transition-all ${
              activeMode === mode.id
                ? `bg-gradient-to-r ${mode.color} bg-opacity-20 border-blue-500`
                : 'bg-gray-800/50 border-gray-700 hover:border-gray-600'
            }`}
            whileHover={{ scale: 1.02 }}
            whileTap={{ scale: 0.98 }}
          >
            <div className="flex items-start gap-3">
              <span className="text-2xl mt-1">{mode.icon}</span>
              <div className="flex-1 min-w-0">
                <h4 className="font-semibold text-white">{mode.label}</h4>
                <p className="text-xs text-gray-400 mt-1">{mode.description}</p>
              </div>
              {activeMode === mode.id && (
                <motion.div
                  initial={{ scale: 0 }}
                  animate={{ scale: 1 }}
                  className="text-blue-400 mt-1"
                >
                  ✓
                </motion.div>
              )}
            </div>
          </motion.button>
        ))}
      </div>

      <AnimatePresence>
        {showConfirm && (
          <motion.div
            className="fixed inset-0 bg-black/50 flex items-center justify-center z-50"
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
          >
            <motion.div
              className="bg-gray-800 p-6 rounded-lg border border-gray-700 max-w-sm mx-4"
              initial={{ scale: 0.9 }}
              animate={{ scale: 1 }}
              exit={{ scale: 0.9 }}
            >
              <h3 className="text-white font-semibold mb-2">Switch Mode?</h3>
              <p className="text-gray-300 text-sm mb-4">
                Your current chat history will be cleared when switching modes.
              </p>
              <div className="flex gap-3">
                <button
                  onClick={() => setShowConfirm(null)}
                  className="flex-1 px-4 py-2 bg-gray-700 hover:bg-gray-600 text-white rounded font-medium transition-colors"
                >
                  Cancel
                </button>
                <button
                  onClick={() => confirmModeChange(showConfirm)}
                  className="flex-1 px-4 py-2 bg-blue-600 hover:bg-blue-700 text-white rounded font-medium transition-colors"
                >
                  Switch
                </button>
              </div>
            </motion.div>
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  )
}
