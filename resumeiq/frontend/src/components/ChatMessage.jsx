import React from 'react'
import { motion } from 'framer-motion'

export const ChatMessage = ({ message, isAI }) => {
  const { role, content, timestamp } = message

  const formatTime = (ts) => {
    if (!ts) return ''
    const date = new Date(ts)
    return date.toLocaleTimeString('en-US', { hour: '2-digit', minute: '2-digit' })
  }

  return (
    <motion.div
      className={`flex ${isAI ? 'justify-start' : 'justify-end'} mb-4`}
      initial={{ opacity: 0, y: 10 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.3 }}
    >
      <div className={`flex gap-3 max-w-md ${isAI ? '' : 'flex-row-reverse'}`}>
        {/* Avatar */}
        <div className={`w-8 h-8 rounded-full flex items-center justify-center flex-shrink-0 ${
          isAI
            ? 'bg-gradient-to-r from-blue-500 to-purple-500'
            : 'bg-gray-700'
        }`}>
          <span className="text-sm font-bold text-white">
            {isAI ? '🤖' : '👤'}
          </span>
        </div>

        {/* Message Bubble */}
        <div className="flex flex-col gap-1">
          <div className={`px-4 py-3 rounded-lg ${
            isAI
              ? 'bg-gray-800 text-gray-100 border border-gray-700'
              : 'bg-blue-600 text-white'
          }`}>
            <p className="text-sm leading-relaxed whitespace-pre-wrap">
              {content}
            </p>
          </div>
          <span className="text-xs text-gray-500 px-2">
            {formatTime(timestamp)}
          </span>
        </div>
      </div>
    </motion.div>
  )
}
