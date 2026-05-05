import React, { useState } from 'react'
import { motion } from 'framer-motion'
import axios from 'axios'
import { useAuth } from '../hooks/useAuth'
import { pageVariants } from '../components/animations'

export const Login = () => {
  const [isSignup, setIsSignup] = useState(false)
  const [email, setEmail] = useState('')
  const [username, setUsername] = useState('')
  const [password, setPassword] = useState('')
  const [error, setError] = useState('')
  const [loading, setLoading] = useState(false)
  const { login } = useAuth()

  const handleSubmit = async (e) => {
    e.preventDefault()
    setError('')
    setLoading(true)

    try {
      const endpoint = isSignup ? '/api/auth/signup' : '/api/auth/login'
      const payload = isSignup
        ? { username, email, password }
        : { email, password }

      const response = await axios.post(`http://localhost:8000${endpoint}`, payload)
      login(response.data.access_token)
      window.location.reload()
    } catch (err) {
      setError(err.response?.data?.detail || 'Error occurred')
    } finally {
      setLoading(false)
    }
  }

  return (
    <motion.div
      className="min-h-screen bg-gradient-to-br from-gray-900 via-gray-800 to-black flex items-center justify-center p-4"
      variants={pageVariants}
      initial="hidden"
      animate="visible"
    >
      <motion.div
        className="w-full max-w-md"
        initial={{ opacity: 0, scale: 0.95 }}
        animate={{ opacity: 1, scale: 1 }}
        transition={{ duration: 0.4 }}
      >
        {/* Header */}
        <motion.div
          className="text-center mb-10"
          initial={{ opacity: 0, y: -20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.1 }}
        >
          <h1 className="text-5xl font-bold text-blue-400 mb-2">ResumeIQ</h1>
          <p className="text-gray-400 text-sm">Transform Your Resume, Advance Your Career</p>
        </motion.div>

        {/* Card */}
        <motion.div
          className="glass-card p-8 rounded-2xl border border-gray-700 bg-gray-900 bg-opacity-50 backdrop-blur-md"
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.2 }}
        >
          {/* Tab Switcher */}
          <motion.div className="flex gap-0 mb-8 bg-gray-800 bg-opacity-50 p-1 rounded-lg">
            <button
              onClick={() => {
                setIsSignup(false)
                setError('')
              }}
              className={`flex-1 py-2 px-4 rounded-md font-medium transition-all ${
                !isSignup
                  ? 'bg-blue-500 text-white shadow-lg'
                  : 'text-gray-400 hover:text-gray-200'
              }`}
            >
              Login
            </button>
            <button
              onClick={() => {
                setIsSignup(true)
                setError('')
              }}
              className={`flex-1 py-2 px-4 rounded-md font-medium transition-all ${
                isSignup
                  ? 'bg-blue-500 text-white shadow-lg'
                  : 'text-gray-400 hover:text-gray-200'
              }`}
            >
              Sign Up
            </button>
          </motion.div>

          {/* Form */}
          <form onSubmit={handleSubmit} className="space-y-5">
            {/* Username Field (Signup only) */}
            {isSignup && (
              <motion.div
                initial={{ opacity: 0, height: 0 }}
                animate={{ opacity: 1, height: 'auto' }}
                exit={{ opacity: 0, height: 0 }}
              >
                <label className="block text-sm font-semibold text-gray-200 mb-2">
                  Username
                </label>
                <input
                  type="text"
                  value={username}
                  onChange={(e) => setUsername(e.target.value)}
                  placeholder="Choose a username"
                  className="w-full px-4 py-3 rounded-lg bg-gray-800 border border-gray-700 text-gray-100 placeholder-gray-500 focus:border-blue-500 focus:ring-1 focus:ring-blue-500 focus:outline-none transition-all"
                  required
                />
              </motion.div>
            )}

            {/* Email Field */}
            <div>
              <label className="block text-sm font-semibold text-gray-200 mb-2">
                Email Address
              </label>
              <input
                type="email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                placeholder="your@email.com"
                className="w-full px-4 py-3 rounded-lg bg-gray-800 border border-gray-700 text-gray-100 placeholder-gray-500 focus:border-blue-500 focus:ring-1 focus:ring-blue-500 focus:outline-none transition-all"
                required
              />
            </div>

            {/* Password Field */}
            <div>
              <label className="block text-sm font-semibold text-gray-200 mb-2">
                Password
              </label>
              <input
                type="password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                placeholder="••••••••"
                className="w-full px-4 py-3 rounded-lg bg-gray-800 border border-gray-700 text-gray-100 placeholder-gray-500 focus:border-blue-500 focus:ring-1 focus:ring-blue-500 focus:outline-none transition-all"
                required
              />
            </div>

            {/* Error Message */}
            {error && (
              <motion.div
                className="bg-red-500 bg-opacity-20 border border-red-500 border-opacity-50 text-red-300 px-4 py-3 rounded-lg text-sm font-medium"
                initial={{ opacity: 0, y: -10 }}
                animate={{ opacity: 1, y: 0 }}
              >
                {error}
              </motion.div>
            )}

            {/* Submit Button */}
            <motion.button
              type="submit"
              disabled={loading}
              className={`w-full py-3 px-4 rounded-lg font-bold transition-all ${
                loading
                  ? 'bg-blue-500 bg-opacity-50 text-gray-300 cursor-not-allowed'
                  : 'bg-gradient-to-r from-blue-500 to-blue-600 text-white hover:shadow-lg hover:shadow-blue-500/50'
              }`}
              whileHover={!loading ? { scale: 1.02 } : {}}
              whileTap={!loading ? { scale: 0.98 } : {}}
            >
              {loading ? (
                <div className="flex items-center justify-center gap-2">
                  <div className="w-4 h-4 border-2 border-gray-300 border-t-white rounded-full animate-spin" />
                  <span>Loading...</span>
                </div>
              ) : isSignup ? (
                'Create Account'
              ) : (
                'Login'
              )}
            </motion.button>
          </form>

          {/* Toggle Signup/Login */}
          <motion.div className="mt-6 text-center text-sm text-gray-400">
            <p>
              {isSignup ? 'Already have an account?' : "Don't have an account?"}
              <button
                onClick={() => {
                  setIsSignup(!isSignup)
                  setError('')
                }}
                className="text-blue-400 hover:text-blue-300 font-semibold ml-2 transition-colors"
              >
                {isSignup ? 'Login Now' : 'Sign Up Now'}
              </button>
            </p>
          </motion.div>
        </motion.div>

        {/* Footer */}
        <motion.p
          className="text-center text-xs text-gray-500 mt-8"
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 0.4 }}
        >
          Secure authentication • No shared data
        </motion.p>
      </motion.div>
    </motion.div>
  )
}
