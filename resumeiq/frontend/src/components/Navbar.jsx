import React from 'react'
import { motion } from 'framer-motion'
import { useAuth } from '../hooks/useAuth'

export const Navbar = ({ onMenuClick }) => {
  const { logout } = useAuth()

  return (
    <motion.nav
      className="bg-gray-900 border-b border-gray-800 px-6 py-4 flex justify-between items-center"
      initial={{ opacity: 0, y: -20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.3 }}
    >
      <div className="flex items-center gap-3">
        <button onClick={onMenuClick} className="text-2xl text-blue-400">☰</button>
        <h1 className="text-2xl font-bold text-blue-400">ResumeIQ</h1>
      </div>
      <motion.button
        onClick={logout}
        className="btn-secondary text-sm"
        whileHover={{ scale: 1.05 }}
        whileTap={{ scale: 0.95 }}
      >
        Logout
      </motion.button>
    </motion.nav>
  )
}
