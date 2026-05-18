import React, { useState, useRef, useEffect } from 'react'
import { motion } from 'framer-motion'
import { SuggestedPrompts } from './SuggestedPrompts'

export const ChatInputArea = ({ onSendMessage, isLoading, mode }) => {
  const [message, setMessage] = useState('')
  const textareaRef = useRef(null)

  useEffect(() => {
    if (textareaRef.current) {
      textareaRef.current.focus()
    }
  }, [mode])

  const handleSend = () => {
    if (message.trim() && !isLoading) {
      onSendMessage(message)
      setMessage('')
      if (textareaRef.current) {
        textareaRef.current.focus()
      }
    }
  }

  const handleKeyDown = (e) => {
    if (e.key === 'Enter' && e.ctrlKey) {
      handleSend()
    }
  }

  const insertPrompt = (prompt) => {
    setMessage(prompt)
    if (textareaRef.current) {
      textareaRef.current.focus()
    }
  }

  return (
    <motion.div
      className="border-t border-gray-700 p-6 space-y-4"
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.3 }}
    >
      <SuggestedPrompts mode={mode} onSelectPrompt={insertPrompt} />

      <div className="flex gap-3">
        <textarea
          ref={textareaRef}
          value={message}
          onChange={(e) => setMessage(e.target.value)}
          onKeyDown={handleKeyDown}
          placeholder="Ask me anything about your career, resume, or interview prep..."
          rows="3"
          disabled={isLoading}
          className="flex-1 px-4 py-3 bg-gray-800 border border-gray-700 rounded-lg text-white placeholder-gray-500 focus:outline-none focus:border-blue-500 focus:ring-1 focus:ring-blue-500/50 resize-none disabled:opacity-50 disabled:cursor-not-allowed"
        />

        <motion.button
          onClick={handleSend}
          disabled={isLoading || !message.trim()}
          className="px-4 py-3 bg-gradient-to-r from-blue-500 to-blue-600 hover:from-blue-600 hover:to-blue-700 text-white rounded-lg font-medium transition-all disabled:opacity-50 disabled:cursor-not-allowed flex-shrink-0"
          whileHover={{ scale: 1.02 }}
          whileTap={{ scale: 0.98 }}
        >
          {isLoading ? (
            <div className="w-6 h-6 border-2 border-blue-200 border-t-white rounded-full animate-spin" />
          ) : (
            '➤'
          )}
        </motion.button>
      </div>

      <p className="text-xs text-gray-500 text-center">
        Ctrl + Enter to send
      </p>
    </motion.div>
  )
}
