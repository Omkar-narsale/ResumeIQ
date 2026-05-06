import React from 'react'
import { motion } from 'framer-motion'

export const ToolkitCard = ({ icon, title, description, onClick, tags = [], isActive = false }) => {
  return (
    <motion.div
      onClick={onClick}
      className={`p-6 rounded-xl border-2 transition-all cursor-pointer backdrop-blur-sm ${
        isActive
          ? 'border-blue-500 bg-blue-500 bg-opacity-20'
          : 'border-gray-700 bg-gray-800 bg-opacity-50 hover:border-blue-400 hover:bg-blue-400 hover:bg-opacity-10'
      }`}
      whileHover={{ scale: 1.05, y: -5 }}
      whileTap={{ scale: 0.98 }}
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.3 }}
    >
      <div className="flex items-start justify-between mb-3">
        <span className="text-4xl">{icon}</span>
        {isActive && (
          <motion.span
            className="text-blue-400"
            initial={{ scale: 0 }}
            animate={{ scale: 1 }}
          >
            ✓
          </motion.span>
        )}
      </div>
      <h3 className="text-lg font-semibold text-white mb-2">{title}</h3>
      <p className="text-sm text-gray-300 mb-4">{description}</p>
      {tags.length > 0 && (
        <div className="flex flex-wrap gap-2">
          {tags.map((tag, i) => (
            <motion.span
              key={i}
              className="px-2 py-1 bg-blue-500 bg-opacity-20 text-blue-300 text-xs rounded-full border border-blue-500 border-opacity-30"
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              transition={{ delay: i * 0.1 }}
            >
              {tag}
            </motion.span>
          ))}
        </div>
      )}
    </motion.div>
  )
}

export const ToolkitSection = ({ title, description, children }) => {
  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.3 }}
      className="space-y-4"
    >
      <div>
        <h2 className="text-2xl font-bold text-white mb-2">{title}</h2>
        <p className="text-gray-400">{description}</p>
      </div>
      {children}
    </motion.div>
  )
}

export const ToolkitFeatureBox = ({ icon, title, items }) => {
  return (
    <motion.div
      className="bg-gradient-to-br from-gray-800 to-gray-900 border border-gray-700 rounded-lg p-6"
      whileHover={{ y: -2, boxShadow: '0 20px 40px rgba(0,0,0,0.3)' }}
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
    >
      <div className="flex items-center gap-3 mb-4">
        <span className="text-3xl">{icon}</span>
        <h3 className="text-lg font-semibold text-white">{title}</h3>
      </div>
      <ul className="space-y-2">
        {items.map((item, i) => (
          <motion.li
            key={i}
            className="text-sm text-gray-300 flex items-center gap-2"
            initial={{ opacity: 0, x: -10 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ delay: i * 0.1 }}
          >
            <span className="text-blue-400">→</span>
            {item}
          </motion.li>
        ))}
      </ul>
    </motion.div>
  )
}
