import React, { useContext, useEffect } from 'react'
import { motion } from 'framer-motion'
import { ChatContext } from '../context/ChatContext'
import { AuthContext } from '../context/AuthContext'
import { ResumeContext } from '../context/ResumeContext'
import { ModeSelector } from '../components/ModeSelector'
import { ChatContainer } from '../components/ChatContainer'
import { ChatInputArea } from '../components/ChatInputArea'
import { Card, CardTitle, CardContent } from '../components/Card'

const pageVariants = {
  hidden: { opacity: 0 },
  visible: { opacity: 1, transition: { duration: 0.3 } }
}

export const CareerCopilot = () => {
  const { activeMode, chatHistory, isLoading, switchMode, clearMode, sendMessage } = useContext(ChatContext)
  const { currentResume } = useContext(ResumeContext)

  const currentMessages = chatHistory[activeMode] || []

  const handleSendMessage = async (message) => {
    await sendMessage(message)
  }

  const handleModeChange = (newMode) => {
    switchMode(newMode)
  }

  const handleClearMode = (mode) => {
    clearMode(mode)
  }

  return (
    <motion.div
      className="h-screen flex flex-col gap-6"
      variants={pageVariants}
      initial="hidden"
      animate="visible"
    >
      {/* Header */}
      <Card>
        <CardTitle>🤖 AI Career Copilot</CardTitle>
        <CardContent className="text-sm text-gray-400">
          Your intelligent career assistant - Get personalized guidance on resume, career strategy, and interviews
        </CardContent>
      </Card>

      {/* Main Layout */}
      <div className="flex-1 grid grid-cols-1 lg:grid-cols-4 gap-6 min-h-0">
        {/* Left Sidebar - Mode Selector */}
        <motion.div
          className="lg:col-span-1"
          initial={{ opacity: 0, x: -20 }}
          animate={{ opacity: 1, x: 0 }}
          transition={{ delay: 0.1, duration: 0.3 }}
        >
          <div className="bg-gray-800/50 rounded-lg border border-gray-700 p-4 sticky top-0">
            <h3 className="text-white font-semibold mb-4 text-sm">Select Mode</h3>
            <ModeSelector
              activeMode={activeMode}
              onModeChange={handleModeChange}
              onClearMode={handleClearMode}
            />
          </div>
        </motion.div>

        {/* Center - Chat Area */}
        <motion.div
          className="lg:col-span-2 flex flex-col bg-gray-800/30 rounded-lg border border-gray-700 overflow-hidden"
          initial={{ opacity: 0, scale: 0.98 }}
          animate={{ opacity: 1, scale: 1 }}
          transition={{ delay: 0.2, duration: 0.3 }}
        >
          <ChatContainer messages={currentMessages} isLoading={isLoading} />
          <ChatInputArea
            onSendMessage={handleSendMessage}
            isLoading={isLoading}
            mode={activeMode}
          />
        </motion.div>

        {/* Right Sidebar - Resume Context */}
        <motion.div
          className="lg:col-span-1"
          initial={{ opacity: 0, x: 20 }}
          animate={{ opacity: 1, x: 0 }}
          transition={{ delay: 0.3, duration: 0.3 }}
        >
          <div className="bg-gray-800/50 rounded-lg border border-gray-700 p-4 sticky top-0 max-h-screen overflow-y-auto">
            <h3 className="text-white font-semibold mb-4 text-sm">📋 Resume Context</h3>

            {currentResume ? (
              <div className="space-y-4 text-sm">
                <div>
                  <p className="text-gray-400 text-xs font-semibold mb-1">FILE</p>
                  <p className="text-white truncate">{currentResume.filename}</p>
                </div>

                {currentResume.extracted_text && (
                  <div>
                    <p className="text-gray-400 text-xs font-semibold mb-2">PREVIEW</p>
                    <p className="text-gray-300 text-xs line-clamp-4 bg-gray-900/50 p-2 rounded">
                      {currentResume.extracted_text.substring(0, 250)}...
                    </p>
                  </div>
                )}

                <div className="pt-4 border-t border-gray-700">
                  <p className="text-gray-400 text-xs font-semibold mb-2">TIPS</p>
                  <ul className="space-y-2 text-xs text-gray-300">
                    <li>✓ Ask for resume feedback by role</li>
                    <li>✓ Mention specific skills to improve</li>
                    <li>✓ Request ATS optimization tips</li>
                    <li>✓ Get interview prep advice</li>
                  </ul>
                </div>
              </div>
            ) : (
              <motion.div
                className="text-center py-8"
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
              >
                <p className="text-gray-400 text-sm mb-2">📄 No Resume Uploaded</p>
                <p className="text-gray-500 text-xs">
                  Upload a resume to get personalized guidance
                </p>
              </motion.div>
            )}

            {/* Quick Stats */}
            <div className="mt-6 pt-4 border-t border-gray-700 space-y-2">
              <div className="flex justify-between items-center">
                <span className="text-gray-400 text-xs">Messages</span>
                <span className="text-white font-semibold">{currentMessages.length}</span>
              </div>
              <div className="flex justify-between items-center">
                <span className="text-gray-400 text-xs">Mode</span>
                <span className="text-blue-400 text-xs font-semibold capitalize">
                  {activeMode.replace('_', ' ')}
                </span>
              </div>
            </div>
          </div>
        </motion.div>
      </div>
    </motion.div>
  )
}
