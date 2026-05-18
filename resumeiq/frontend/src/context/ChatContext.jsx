import React, { createContext, useState, useCallback, useContext } from 'react'
import { AuthContext } from './AuthContext'
import { ResumeContext } from './ResumeContext'

export const ChatContext = createContext()

export const ChatProvider = ({ children }) => {
  const { token } = useContext(AuthContext)
  const { currentResume } = useContext(ResumeContext)

  const [activeMode, setActiveMode] = useState('career_mentor')
  const [chatHistory, setChatHistory] = useState({
    resume_expert: [],
    career_mentor: [],
    interview_coach: []
  })
  const [resumeContext, setResumeContext] = useState(null)
  const [isLoading, setIsLoading] = useState(false)

  const addMessage = useCallback((mode, role, content) => {
    setChatHistory(prev => ({
      ...prev,
      [mode]: [...prev[mode], { role, content, timestamp: new Date().toISOString() }]
    }))
  }, [])

  const clearMode = useCallback((mode) => {
    setChatHistory(prev => ({
      ...prev,
      [mode]: []
    }))
  }, [])

  const switchMode = useCallback((newMode) => {
    setActiveMode(newMode)
  }, [])

  const sendMessage = useCallback(async (userMessage) => {
    if (!userMessage.trim() || !token) return null

    addMessage(activeMode, 'user', userMessage)
    setIsLoading(true)

    try {
      const resume = resumeContext || currentResume
      const resumeContextPayload = resume ? {
        extracted_text: resume.extracted_text,
        skills: resume.skills || []
      } : null

      const response = await fetch('http://localhost:8000/api/chat', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify({
          user_message: userMessage,
          mode: activeMode,
          resume_context: resumeContextPayload,
          conversation_history: chatHistory[activeMode]
        })
      })

      if (!response.ok) {
        throw new Error('Failed to get response')
      }

      const data = await response.json()
      addMessage(activeMode, 'assistant', data.response)

      return data.response
    } catch (error) {
      console.error('Chat error:', error)
      const errorMessage = 'Sorry, I encountered an error. Could you try again?'
      addMessage(activeMode, 'assistant', errorMessage)
      return null
    } finally {
      setIsLoading(false)
    }
  }, [activeMode, token, chatHistory, resumeContext, currentResume, addMessage])

  const fetchHistory = useCallback(async (mode) => {
    if (!token) return

    try {
      const response = await fetch(`http://localhost:8000/api/chat/history?mode=${mode}`, {
        headers: {
          'Authorization': `Bearer ${token}`
        }
      })

      if (!response.ok) return

      const data = await response.json()
      setChatHistory(prev => ({
        ...prev,
        [mode]: data.messages.map(msg => ({
          role: msg.role,
          content: msg.content,
          timestamp: msg.created_at
        }))
      }))
    } catch (error) {
      console.error('Failed to fetch chat history:', error)
    }
  }, [token])

  const value = {
    activeMode,
    chatHistory,
    resumeContext,
    isLoading,
    addMessage,
    clearMode,
    switchMode,
    sendMessage,
    fetchHistory,
    setResumeContext
  }

  return (
    <ChatContext.Provider value={value}>
      {children}
    </ChatContext.Provider>
  )
}
