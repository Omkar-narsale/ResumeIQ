import React, { useState } from 'react'
import { motion, AnimatePresence } from 'framer-motion'

export const MenuGroup = ({
  group,
  currentPage,
  onNavigate,
  resume,
  onClose
}) => {
  const [isOpen, setIsOpen] = useState(false)

  const hasActiveItem = group.items.some(item => item.id === currentPage)

  return (
    <div className="space-y-1">
      {/* Group Header */}
      <motion.button
        onClick={() => setIsOpen(!isOpen)}
        className={`w-full text-left px-4 py-3 rounded-lg transition-all flex items-center justify-between ${
          hasActiveItem
            ? 'bg-blue-500 text-white shadow-lg shadow-blue-500/50'
            : 'text-gray-300 hover:bg-gray-800 hover:text-white'
        }`}
        whileHover={{ x: 5 }}
        whileTap={{ scale: 0.98 }}
      >
        <div className="flex items-center gap-3">
          <span className="text-lg flex-shrink-0">{group.icon}</span>
          <span className="font-medium text-sm">{group.label}</span>
        </div>
        <motion.span
          animate={{ rotate: isOpen ? 180 : 0 }}
          transition={{ duration: 0.3 }}
          className="text-xs"
        >
          ▼
        </motion.span>
      </motion.button>

      {/* Group Items */}
      <AnimatePresence>
        {isOpen && (
          <motion.div
            initial={{ opacity: 0, height: 0 }}
            animate={{ opacity: 1, height: 'auto' }}
            exit={{ opacity: 0, height: 0 }}
            transition={{ duration: 0.2 }}
            className="space-y-1 overflow-hidden"
          >
            {group.items.map((item) => {
              const isEnabled = item.alwaysEnabled || resume
              const isDisabled = !isEnabled
              const isActive = currentPage === item.id

              return (
                <motion.button
                  key={item.id}
                  onClick={() => {
                    if (!isDisabled) {
                      onNavigate(item.id)
                      onClose()
                    }
                  }}
                  initial={{ opacity: 0, x: -10 }}
                  animate={{ opacity: 1, x: 0 }}
                  exit={{ opacity: 0, x: -10 }}
                  transition={{ duration: 0.2 }}
                  className={`w-full text-left px-6 py-2 rounded-lg transition-all flex items-center gap-2 text-sm ml-2 border-l-2 ${
                    isDisabled
                      ? 'opacity-40 cursor-not-allowed border-gray-700 text-gray-600'
                      : isActive
                      ? 'border-blue-400 bg-blue-500 bg-opacity-20 text-blue-300 font-medium'
                      : 'border-gray-700 text-gray-400 hover:text-gray-200 hover:border-gray-600'
                  }`}
                  whileHover={!isDisabled ? { x: 3 } : {}}
                  whileTap={!isDisabled ? { scale: 0.97 } : {}}
                  title={isDisabled ? 'Upload resume to unlock' : ''}
                >
                  <span className="text-base flex-shrink-0">{item.icon}</span>
                  <span>{item.label}</span>
                </motion.button>
              )
            })}
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  )
}
