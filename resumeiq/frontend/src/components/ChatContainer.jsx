import React, { useEffect, useRef } from 'react'
import { motion } from 'framer-motion'
import { ChatMessage } from './ChatMessage'

export const ChatContainer = ({ messages, isLoading }) => {
  const messagesEndRef = useRef(null)

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }

  useEffect(() => {
    scrollToBottom()
  }, [messages])

  return (
    <div className="flex-1 overflow-y-auto p-6 space-y-4">
      {messages.length === 0 ? (
        <motion.div
          className="h-full flex items-center justify-center text-center"
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
        >
          <div>
            <p className="text-4xl mb-3">💬</p>
            <p className="text-gray-400 text-sm">
              Start your conversation with the AI Career Copilot
            </p>
            <p className="text-gray-500 text-xs mt-2">
              Choose a mode and ask any career-related question
            </p>
          </div>
        </motion.div>
      ) : (
        <>
          {messages.map((msg, idx) => (
            <ChatMessage
              key={idx}
              message={msg}
              isAI={msg.role === 'assistant'}
            />
          ))}
          {isLoading && (
            <motion.div
              className="flex justify-start mb-4"
              initial={{ opacity: 0, y: 10 }}
              animate={{ opacity: 1, y: 0 }}
            >
              <div className="flex gap-3">
                <div className="w-8 h-8 rounded-full bg-gradient-to-r from-blue-500 to-purple-500 flex items-center justify-center">
                  <span className="text-sm font-bold">🤖</span>
                </div>
                <div className="bg-gray-800 px-4 py-3 rounded-lg border border-gray-700">
                  <div className="flex gap-1">
                    <motion.div
                      className="w-2 h-2 bg-gray-500 rounded-full"
                      animate={{ y: [0, -8, 0] }}
                      transition={{ duration: 0.6, repeat: Infinity }}
                    />
                    <motion.div
                      className="w-2 h-2 bg-gray-500 rounded-full"
                      animate={{ y: [0, -8, 0] }}
                      transition={{ duration: 0.6, delay: 0.1, repeat: Infinity }}
                    />
                    <motion.div
                      className="w-2 h-2 bg-gray-500 rounded-full"
                      animate={{ y: [0, -8, 0] }}
                      transition={{ duration: 0.6, delay: 0.2, repeat: Infinity }}
                    />
                  </div>
                </div>
              </div>
            </motion.div>
          )}
          <div ref={messagesEndRef} />
        </>
      )}
    </div>
  )
}
