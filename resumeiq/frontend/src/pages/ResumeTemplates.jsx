import React, { useState } from 'react'
import { motion } from 'framer-motion'
import { Card, CardTitle, CardContent } from '../components/Card'
import { useResume } from '../hooks/useResume'
import { useAuth } from '../hooks/useAuth'
import { pageVariants, containerVariants, itemVariants } from '../components/animations'

const templates = [
  {
    id: 'modern',
    name: 'Modern',
    description: 'Clean, contemporary design for tech companies',
    styles: 'bg-white text-gray-900 p-8 font-sans'
  },
  {
    id: 'classic',
    name: 'Classic',
    description: 'Professional, traditional format for corporate roles',
    styles: 'bg-gray-100 text-gray-900 border-l-4 border-blue-600 pl-6 py-2 font-serif'
  },
  {
    id: 'minimal',
    name: 'Minimal',
    description: 'Minimalist design for creative professionals',
    styles: 'bg-gray-50 text-gray-900 p-6 font-sans tracking-tight'
  }
]

export const ResumeTemplates = () => {
  const [selectedTemplate, setSelectedTemplate] = useState('modern')
  const [isDownloading, setIsDownloading] = useState(false)
  const { resume } = useResume()
  const { token } = useAuth()

  const handleDownload = async (format) => {
    if (!resume) {
      alert('Please upload a resume first')
      return
    }

    setIsDownloading(true)
    try {
      const response = await fetch('http://localhost:8000/api/download-resume', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify({
          resume: resume,
          format: format.toLowerCase()
        })
      })

      if (!response.ok) {
        const errorText = await response.text()
        throw new Error(`Download failed: ${response.status} - ${errorText}`)
      }

      const blob = await response.blob()
      const url = window.URL.createObjectURL(blob)
      const a = document.createElement('a')
      a.href = url
      a.download = `resume_${selectedTemplate}.${format === 'PDF' ? 'pdf' : format === 'DOCX' ? 'docx' : 'txt'}`
      document.body.appendChild(a)
      a.click()
      window.URL.revokeObjectURL(url)
      document.body.removeChild(a)
      alert(`Resume downloaded as ${format}!`)
    } catch (error) {
      console.error('Download error:', error)
      alert(`Error downloading resume: ${error.message}`)
    } finally {
      setIsDownloading(false)
    }
  }

  return (
    <motion.div
      className="space-y-6"
      variants={pageVariants}
      initial="hidden"
      animate="visible"
    >
      <Card>
        <CardTitle>🎨 Resume Templates</CardTitle>
        <CardContent className="text-sm text-gray-400">
          Choose a template design and preview your resume in different formats
        </CardContent>
      </Card>

      {/* Template Selection */}
      <motion.div variants={containerVariants} className="grid grid-cols-1 md:grid-cols-3 gap-4">
        {templates.map((template) => (
          <motion.div
            key={template.id}
            variants={itemVariants}
            onClick={() => setSelectedTemplate(template.id)}
            className={`p-4 rounded-lg border-2 cursor-pointer transition-all ${
              selectedTemplate === template.id
                ? 'border-blue-500 bg-blue-500 bg-opacity-10'
                : 'border-gray-700 hover:border-gray-600'
            }`}
            whileHover={{ scale: 1.05 }}
          >
            <div className="font-semibold mb-1">{template.name}</div>
            <div className="text-xs text-gray-400">{template.description}</div>
          </motion.div>
        ))}
      </motion.div>

      {resume && (
        <>
          {/* Preview */}
          <motion.div variants={itemVariants}>
            <Card>
              <CardTitle>👁️ Preview</CardTitle>
              <CardContent>
                <div className={`rounded-lg p-6 max-h-96 overflow-y-auto ${templates.find(t => t.id === selectedTemplate).styles}`}>
                  {resume.split('\n').slice(0, 20).map((line, i) => (
                    <div key={i} className="whitespace-pre-wrap break-words">
                      {line}
                    </div>
                  ))}
                </div>
              </CardContent>
            </Card>
          </motion.div>

          {/* Export Options */}
          <motion.div variants={itemVariants}>
            <Card>
              <CardTitle>📥 Export Options</CardTitle>
              <CardContent className="grid grid-cols-1 md:grid-cols-3 gap-3">
                {['PDF', 'DOCX', 'TXT'].map((format) => (
                  <motion.button
                    key={format}
                    onClick={() => handleDownload(format)}
                    disabled={isDownloading}
                    className={`btn-primary text-sm ${isDownloading ? 'opacity-50 cursor-not-allowed' : ''}`}
                    whileHover={!isDownloading ? { scale: 1.05 } : {}}
                    whileTap={!isDownloading ? { scale: 0.95 } : {}}
                  >
                    {isDownloading ? '⏳ Downloading...' : `📄 Download ${format}`}
                  </motion.button>
                ))}
              </CardContent>
            </Card>
          </motion.div>

          {/* Template Info */}
          <motion.div variants={itemVariants}>
            <Card>
              <CardTitle>💡 Template Tips</CardTitle>
              <CardContent className="space-y-2 text-sm text-gray-300">
                <div>
                  <strong>Modern:</strong> Best for tech, startups, and creative roles
                </div>
                <div>
                  <strong>Classic:</strong> Best for corporate, finance, and traditional industries
                </div>
                <div>
                  <strong>Minimal:</strong> Best for design, consulting, and leadership roles
                </div>
              </CardContent>
            </Card>
          </motion.div>
        </>
      )}

      {!resume && (
        <motion.div
          className="bg-yellow-500 bg-opacity-20 border border-yellow-500 text-yellow-300 p-4 rounded-lg"
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
        >
          📄 Upload a resume first to preview templates
        </motion.div>
      )}
    </motion.div>
  )
}
