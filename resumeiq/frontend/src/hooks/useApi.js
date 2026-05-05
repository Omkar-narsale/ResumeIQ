import { useState } from 'react'
import axios from 'axios'
import { useAuth } from './useAuth'

const API_BASE = 'http://localhost:8000'

export const useApi = () => {
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)
  const { token } = useAuth()

  const call = async (method, endpoint, data = null) => {
    setLoading(true)
    setError(null)
    try {
      const config = {
        method,
        url: `${API_BASE}${endpoint}`,
        headers: {
          'Content-Type': 'application/json',
          ...(token && { 'Authorization': `Bearer ${token}` })
        }
      }
      if (data) config.data = data

      const response = await axios(config)
      return response.data
    } catch (err) {
      const msg = err.response?.data?.detail || err.message || 'Error'
      setError(msg)
      throw err
    } finally {
      setLoading(false)
    }
  }

  return { call, loading, error }
}
