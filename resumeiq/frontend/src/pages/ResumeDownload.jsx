import React, { useState } from 'react'
import { motion } from 'framer-motion'
import { Card, CardTitle, CardContent } from '../components/Card'
import { useApi } from '../hooks/useApi'
import { useResume } from '../hooks/useResume'
import { pageVariants, containerVariants, itemVariants } from '../components/animations'

export const ResumeDownload = () => {
  const [format, setFormat] = useState('pdf')
  const [customText, setCustomText] = useState('')
  const [downloading, setDownloading] = useState(false)
  const { resume } = useResume()
  const { call, error } = useApi()

  const handleDownload = async () => {
    if (!resume && !customText) {
      alert('Please upload a resume or paste text')
      return
    }

    setDownloading(true)
    try {
      const resumeText = customText || resume
      const response = await fetch('http://localhost:8000/api/download-resume', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${localStorage.getItem('token')}`
        },
        body: JSON.stringify({
          resume: resumeText.slice(0, 5000),
          format: format
        })
      })

      if (!response.ok) throw new Error('Download failed')

      const blob = await response.blob()
      const url = window.URL.createObjectURL(blob)
      const link = document.createElement('a')
      link.href = url
      link.download = `resume.${format}`
      document.body.appendChild(link)
      link.click()
      document.body.removeChild(link)
      window.URL.revokeObjectURL(url)
    } catch (err) {
      console.error('Download failed:', err)
      alert('Download failed. Please try again.')
    } finally {
      setDownloading(false)
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
        <CardTitle>📥 Download Resume</CardTitle>
        <p className="text-gray-400 text-sm mb-4">Download your resume in PDF or DOCX format</p>
      </Card>

      <motion.div
        className="grid grid-cols-1 md:grid-cols-2 gap-6"
        variants={containerVariants}
        initial="hidden"
        animate="visible"
      >
        <motion.div variants={itemVariants}>
          <Card>
            <CardTitle>📄 Current Resume</CardTitle>
            <CardContent>
              {resume ? (
                <div className="space-y-3">
                  <div className="bg-gray-800 p-3 rounded max-h-40 overflow-auto text-sm text-gray-300">
                    {resume.substring(0, 400)}...
                  </div>
                  <p className="text-xs text-gray-400">
                    {resume.split(' ').length} words
                  </p>
                </div>
              ) : (
                <p className="text-gray-400 text-sm py-4">No resume uploaded</p>
              )}
            </CardContent>
          </Card>
        </motion.div>

        <motion.div variants={itemVariants}>
          <Card>
            <CardTitle>⚙️ Download Options</CardTitle>
            <CardContent>
              <div className="space-y-4">
                <div>
                  <label className="block text-sm font-medium mb-3">Choose Format:</label>
                  <div className="grid grid-cols-2 gap-3">
                    <motion.button
                      onClick={() => setFormat('pdf')}
                      className={`p-3 rounded border-2 transition-all ${
                        format === 'pdf'
                          ? 'border-blue-500 bg-blue-500 bg-opacity-20'
                          : 'border-gray-600 hover:border-gray-500'
                      }`}
                      whileHover={{ scale: 1.05 }}
                      whileTap={{ scale: 0.95 }}
                    >
                      <div className="text-xl mb-1">📕</div>
                      <div className="text-sm font-semibold">PDF</div>
                    </motion.button>

                    <motion.button
                      onClick={() => setFormat('docx')}
                      className={`p-3 rounded border-2 transition-all ${
                        format === 'docx'
                          ? 'border-blue-500 bg-blue-500 bg-opacity-20'
                          : 'border-gray-600 hover:border-gray-500'
                      }`}
                      whileHover={{ scale: 1.05 }}
                      whileTap={{ scale: 0.95 }}
                    >
                      <div className="text-xl mb-1">📗</div>
                      <div className="text-sm font-semibold">DOCX</div>
                    </motion.button>
                  </div>
                </div>

                <motion.button
                  onClick={handleDownload}
                  disabled={downloading || (!resume && !customText)}
                  className="w-full btn-primary"
                  whileHover={{ scale: 1.02 }}
                  whileTap={{ scale: 0.98 }}
                >
                  {downloading ? 'Downloading...' : `Download as ${format.toUpperCase()}`}
                </motion.button>
              </div>
            </CardContent>
          </Card>
        </motion.div>
      </motion.div>

      {!resume && (
        <motion.div variants={itemVariants}>
          <Card>
            <CardTitle>✏️ Or Paste Resume Text</CardTitle>
            <CardContent>
              <label className="block text-sm font-medium mb-2">Resume Text:</label>
              <textarea
                value={customText}
                onChange={(e) => setCustomText(e.target.value)}
                placeholder="Paste your resume here if no file is uploaded..."
                className="w-full h-40 resize-none"
                maxLength={5000}
              />
              <p className="text-xs text-gray-400 mt-2">{customText.length}/5000 characters</p>
            </CardContent>
          </Card>
        </motion.div>
      )}

      <motion.div variants={itemVariants}>
        <Card>
          <CardTitle>📋 Format Comparison</CardTitle>
          <CardContent>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div className="border-l-4 border-blue-500 pl-4">
                <p className="font-semibold mb-2">📕 PDF Format</p>
                <ul className="text-sm text-gray-300 space-y-1">
                  <li>✓ Universal format (opens anywhere)</li>
                  <li>✓ Preserves exact formatting</li>
                  <li>✓ Professional appearance</li>
                  <li>✓ Best for email/online applications</li>
                </ul>
              </div>
              <div className="border-l-4 border-green-500 pl-4">
                <p className="font-semibold mb-2">📗 DOCX Format</p>
                <ul className="text-sm text-gray-300 space-y-1">
                  <li>✓ Editable in Word/Google Docs</li>
                  <li>✓ Easy to customize further</li>
                  <li>✓ ATS system compatible</li>
                  <li>✓ Best for personalization</li>
                </ul>
              </div>
            </div>
          </CardContent>
        </Card>
      </motion.div>

      <motion.div variants={itemVariants}>
        <Card>
          <CardTitle>💡 Download Tips</CardTitle>
          <CardContent>
            <ul className="space-y-2 text-sm text-gray-300">
              <li>✓ Use PDF for most job applications (cleaner formatting)</li>
              <li>✓ Use DOCX when company asks for editable version</li>
              <li>✓ Download multiple versions for different jobs</li>
              <li>✓ Keep file name professional (FirstName_LastName_Resume.pdf)</li>
            </ul>
          </CardContent>
        </Card>
      </motion.div>

      {error && (
        <motion.div
          className="bg-red-500 bg-opacity-20 border border-red-500 text-red-300 p-3 rounded-lg"
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
        >
          {error}
        </motion.div>
      )}
    </motion.div>
  )
}
