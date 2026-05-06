import React from 'react'
import { motion } from 'framer-motion'
import { sidebarVariants } from './animations'
import { useResume } from '../hooks/useResume'
import { MenuGroup } from './MenuGroup'
import { navConfig } from '../config/navConfig'

export const Sidebar = ({ isOpen, currentPage, onNavigate, onClose }) => {
  const { resume } = useResume()

  return (
    <>
      {/* Backdrop */}
      {isOpen && (
        <motion.div
          className="fixed inset-0 bg-black bg-opacity-50 z-40 md:hidden"
          onClick={onClose}
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          exit={{ opacity: 0 }}
        />
      )}

      {/* Sidebar */}
      <motion.aside
        className={`fixed md:relative left-0 top-0 w-64 h-screen bg-gradient-to-b from-gray-900 to-gray-950 border-r border-gray-800 p-6 z-50 overflow-y-auto ${
          isOpen ? 'block' : 'hidden md:block'
        }`}
        variants={sidebarVariants}
        initial="hidden"
        animate="visible"
      >
        {/* Logo */}
        <motion.div className="mb-8 pb-4 border-b border-gray-800">
          <h2 className="text-xl font-bold text-blue-400">ResumeIQ</h2>
          <p className="text-xs text-gray-500">Career Intelligence</p>
        </motion.div>

        {/* Navigation */}
        <nav className="space-y-3">
          {navConfig.map((item) => {
            if (item.type === 'group') {
              return (
                <MenuGroup
                  key={item.id}
                  group={item}
                  currentPage={currentPage}
                  onNavigate={onNavigate}
                  resume={resume}
                  onClose={onClose}
                />
              )
            } else {
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
                  className={`w-full text-left px-4 py-3 rounded-lg transition-all flex items-center gap-3 ${
                    isDisabled
                      ? 'opacity-40 cursor-not-allowed bg-gray-900 text-gray-600'
                      : isActive
                      ? 'bg-blue-500 text-white shadow-lg shadow-blue-500/50'
                      : 'text-gray-300 hover:bg-gray-800 hover:text-white'
                  }`}
                  whileHover={!isDisabled ? { x: 5 } : {}}
                  whileTap={!isDisabled ? { scale: 0.98 } : {}}
                  title={isDisabled ? 'Upload resume to unlock' : ''}
                >
                  <span className="text-lg flex-shrink-0">{item.icon}</span>
                  <span className="font-medium text-sm">{item.label}</span>
                </motion.button>
              )
            }
          })}
        </nav>

        {/* Resume Status */}
        {!resume && (
          <motion.div
            className="mt-auto pt-6 border-t border-gray-800"
            initial={{ opacity: 0, y: 10 }}
            animate={{ opacity: 1, y: 0 }}
          >
            <div className="p-4 bg-yellow-500 bg-opacity-15 border border-yellow-500 border-opacity-50 rounded-lg text-yellow-400 text-xs">
              <p className="font-semibold mb-1">📂 Resume Locked</p>
              <p>Upload your resume to unlock all features</p>
            </div>
          </motion.div>
        )}

        {resume && (
          <motion.div
            className="mt-auto pt-6 border-t border-gray-800"
            initial={{ opacity: 0, y: 10 }}
            animate={{ opacity: 1, y: 0 }}
          >
            <div className="p-3 bg-green-500 bg-opacity-15 border border-green-500 border-opacity-50 rounded-lg text-green-400 text-xs text-center font-semibold">
              ✅ Resume Active
            </div>
          </motion.div>
        )}
      </motion.aside>
    </>
  )
}
