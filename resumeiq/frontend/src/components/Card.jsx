import React from 'react'
import { motion } from 'framer-motion'
import { cardVariants } from './animations'

export const Card = ({ children, className = '', hover = true }) => {
  return (
    <motion.div
      className={`glass-card p-6 ${className}`}
      variants={hover ? cardVariants : {}}
      initial="hidden"
      animate="visible"
      whileHover={hover ? "hover" : {}}
    >
      {children}
    </motion.div>
  )
}

export const CardTitle = ({ children }) => (
  <h2 className="text-2xl font-bold mb-4 text-blue-400">{children}</h2>
)

export const CardContent = ({ children }) => (
  <div className="text-gray-300">{children}</div>
)
