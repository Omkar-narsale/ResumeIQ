import React from 'react'
import { motion } from 'framer-motion'
import { cardVariants } from './animations'

export const MetricCard = ({ title, value, icon, color = 'blue' }) => {
  const colorClasses = {
    blue: 'from-blue-500 to-blue-600',
    green: 'from-green-500 to-green-600',
    purple: 'from-purple-500 to-purple-600',
    orange: 'from-orange-500 to-orange-600',
  }

  return (
    <motion.div
      className={`glass-card p-6 gradient-${color}`}
      variants={cardVariants}
      initial="hidden"
      animate="visible"
      whileHover="hover"
    >
      <div className="flex items-center justify-between mb-4">
        <h3 className="text-gray-200 text-sm font-semibold uppercase">{title}</h3>
        <span className="text-3xl">{icon}</span>
      </div>
      <motion.div
        className="text-4xl font-bold text-white"
        initial={{ opacity: 0, y: 10 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.2, duration: 0.5 }}
      >
        {value}
      </motion.div>
    </motion.div>
  )
}
