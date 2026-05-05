import React, { createContext, useState, useEffect } from 'react'
import axios from 'axios'
import { useAuth } from '../hooks/useAuth'

export const ResumeContext = createContext()

export const ResumeProvider = ({ children }) => {
  const [resume, setResume] = useState(null)
  const [resumeId, setResumeId] = useState(null)
  const [resumes, setResumes] = useState([])
  const [loading, setLoading] = useState(false)
  const [autoAnalysis, setAutoAnalysis] = useState(null)
  const { token } = useAuth()

  const API_BASE = 'http://localhost:8000'

  useEffect(() => {
    if (token) {
      loadCurrentResume()
    }
  }, [token])

  const loadCurrentResume = async () => {
    try {
      const response = await fetch(`${API_BASE}/api/current-resume`, {
        headers: { 'Authorization': `Bearer ${token}` }
      })
      if (response.ok) {
        const data = await response.json()
        if (data) {
          setResume(data.extracted_text)
          setResumeId(data.id)
        }
      }
    } catch (error) {
      console.error('Error loading resume:', error)
    }
  }

  const uploadResume = async (file) => {
    setLoading(true)
    try {
      const formData = new FormData()
      formData.append('file', file)

      const response = await fetch(`${API_BASE}/api/resumes/upload`, {
        method: 'POST',
        headers: { 'Authorization': `Bearer ${token}` },
        body: formData
      })

      if (!response.ok) {
        throw new Error('Upload failed')
      }

      const data = await response.json()
      setResume(data.extracted_text)
      setResumeId(data.id)
      await loadResumes()

      // Auto-trigger analysis after successful upload
      await triggerAutoAnalysis(data.extracted_text)

      return data
    } catch (error) {
      console.error('Upload error:', error)
      throw error
    } finally {
      setLoading(false)
    }
  }

  const triggerAutoAnalysis = async (resumeText) => {
    try {
      const response = await axios.post(
        `${API_BASE}/api/analyze`,
        { text: resumeText },
        { headers: { 'Authorization': `Bearer ${token}` } }
      )
      setAutoAnalysis(response.data)
    } catch (err) {
      console.error('Auto-analysis failed (non-blocking):', err)
      // Don't throw - auto-analysis failure shouldn't break upload
    }
  }

  const loadResumes = async () => {
    try {
      const response = await fetch(`${API_BASE}/api/resumes`, {
        headers: { 'Authorization': `Bearer ${token}` }
      })
      if (response.ok) {
        const data = await response.json()
        setResumes(data)
      }
    } catch (error) {
      console.error('Error loading resumes:', error)
    }
  }

  const selectResume = async (id) => {
    try {
      const response = await fetch(`${API_BASE}/api/resumes/${id}/select`, {
        method: 'POST',
        headers: { 'Authorization': `Bearer ${token}` }
      })
      if (response.ok) {
        await loadCurrentResume()
        await loadResumes()
        setAutoAnalysis(null)
      }
    } catch (error) {
      console.error('Error selecting resume:', error)
    }
  }

  const deleteResume = async (id) => {
    try {
      const response = await fetch(`${API_BASE}/api/resumes/${id}`, {
        method: 'DELETE',
        headers: { 'Authorization': `Bearer ${token}` }
      })
      if (response.ok) {
        await loadResumes()
        if (resumeId === id) {
          setResume(null)
          setResumeId(null)
          setAutoAnalysis(null)
        }
      }
    } catch (error) {
      console.error('Error deleting resume:', error)
    }
  }

  return (
    <ResumeContext.Provider value={{
      resume,
      resumeId,
      resumes,
      loading,
      autoAnalysis,
      uploadResume,
      selectResume,
      deleteResume,
      loadResumes,
      loadCurrentResume
    }}>
      {children}
    </ResumeContext.Provider>
  )
}
