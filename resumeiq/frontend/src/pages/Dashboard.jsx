import React, { useState, useEffect } from 'react'
import { motion } from 'framer-motion'
import { Card, CardTitle, CardContent } from '../components/Card'
import { useApi } from '../hooks/useApi'
import { useAuth } from '../hooks/useAuth'
import { useResume } from '../hooks/useResume'
import { pageVariants, containerVariants, itemVariants } from '../components/animations'

// CSS Animations
const chartStyles = `
  @keyframes drawGauge {
    from {
      stroke-dashoffset: 282.74;
    }
    to {
      stroke-dashoffset: var(--offset, 282.74);
    }
  }

  @keyframes slideUp {
    from {
      opacity: 0;
      transform: translateY(20px);
    }
    to {
      opacity: 1;
      transform: translateY(0);
    }
  }

  @keyframes scaleIn {
    from {
      opacity: 0;
      transform: scale(0.8);
    }
    to {
      opacity: 1;
      transform: scale(1);
    }
  }

  @keyframes pulse-glow {
    0%, 100% {
      box-shadow: 0 0 0 0 rgba(59, 130, 246, 0.7);
    }
    50% {
      box-shadow: 0 0 0 10px rgba(59, 130, 246, 0);
    }
  }

  .gauge-circle {
    animation: drawGauge 1.5s ease-out forwards;
  }

  .chart-container {
    animation: slideUp 0.6s ease-out;
  }

  .stat-card {
    transition: all 0.3s ease;
  }

  .stat-card:hover {
    transform: translateY(-4px);
    box-shadow: 0 12px 24px rgba(59, 130, 246, 0.2);
    border-color: rgba(59, 130, 246, 0.6);
  }

  .insight-card {
    transition: all 0.3s ease;
  }

  .insight-card:hover {
    transform: translateY(-4px);
    box-shadow: 0 12px 24px rgba(59, 130, 246, 0.15);
  }

  .action-card {
    transition: all 0.3s cubic-bezier(0.34, 1.56, 0.64, 1);
    position: relative;
    overflow: hidden;
  }

  .action-card::before {
    content: '';
    position: absolute;
    top: 0;
    left: -100%;
    width: 100%;
    height: 100%;
    background: rgba(255, 255, 255, 0.1);
    transition: left 0.3s ease;
  }

  .action-card:hover::before {
    left: 100%;
  }

  .action-card:hover {
    transform: scale(1.05) translateY(-8px);
    box-shadow: 0 20px 40px rgba(59, 130, 246, 0.4);
  }

  .progress-bar-container {
    animation: slideUp 0.5s ease-out forwards;
  }

  .progress-fill {
    animation: fillProgress 1.2s cubic-bezier(0.34, 1.56, 0.64, 1) forwards;
  }

  @keyframes fillProgress {
    from {
      width: 0%;
    }
    to {
      width: var(--value, 100%);
    }
  }

  .radar-path {
    animation: scaleIn 0.8s ease-out 0.2s forwards;
    opacity: 0;
  }

  .stepper-ball {
    animation: pulse-glow 2s infinite;
  }
`

// Gauge Chart Component with proper animation
const GaugeChart = ({ score = 7.5 }) => {
  const circumference = 2 * Math.PI * 45
  const offset = circumference - (score / 10) * circumference
  const color = score >= 8 ? '#10b981' : score >= 6 ? '#f59e0b' : '#ef4444'

  return (
    <motion.div
      className="flex flex-col items-center justify-center"
      initial={{ opacity: 0, scale: 0.8 }}
      animate={{ opacity: 1, scale: 1 }}
      transition={{ duration: 0.6 }}
    >
      <svg width="180" height="180" className="transform -rotate-90" style={{ filter: 'drop-shadow(0 0 20px rgba(59, 130, 246, 0.2))' }}>
        {/* Background circle */}
        <circle cx="90" cy="90" r="45" fill="none" stroke="#374151" strokeWidth="8" />

        {/* Animated gauge */}
        <circle
          cx="90"
          cy="90"
          r="45"
          fill="none"
          stroke={color}
          strokeWidth="8"
          strokeDasharray={circumference}
          strokeDashoffset={circumference}
          style={{
            '--offset': offset,
            animation: `drawGauge 1.5s cubic-bezier(0.34, 1.56, 0.64, 1) forwards`,
          }}
          strokeLinecap="round"
        />
      </svg>
      <motion.div
        className="absolute text-center"
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ delay: 0.8 }}
      >
        <p className="text-4xl font-bold text-white">{score.toFixed(1)}</p>
        <p className="text-sm text-gray-400">/10</p>
      </motion.div>
    </motion.div>
  )
}

// Animated Skill Radar with proper drawing
const SkillRadar = ({ skills = { Python: 8, SQL: 7, ML: 6, Visualization: 5, Communication: 8 } }) => {
  const entries = Object.entries(skills)
  const angle = (360 / entries.length) * (Math.PI / 180)
  const [animationComplete, setAnimationComplete] = useState(false)

  const points = entries.map((_, i) => {
    const x = 100 + 80 * Math.cos(i * angle - Math.PI / 2)
    const y = 100 + 80 * Math.sin(i * angle - Math.PI / 2)
    return [x, y]
  })

  const polygonPoints = points.map(p => p.join(',')).join(' ')

  return (
    <motion.div
      className="flex justify-center chart-container"
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      onAnimationComplete={() => setAnimationComplete(true)}
    >
      <svg viewBox="0 0 200 200" className="w-full h-64" style={{ filter: 'drop-shadow(0 0 15px rgba(59, 130, 246, 0.15))' }}>
        {/* Background circles */}
        {[1, 2, 3, 4].map(i => (
          <circle
            key={`bg-${i}`}
            cx="100"
            cy="100"
            r={20 * i}
            fill="none"
            stroke="#374151"
            strokeWidth="0.5"
            opacity="0.5"
          />
        ))}

        {/* Axes */}
        {entries.map((_, i) => {
          const x = 100 + 80 * Math.cos(i * angle - Math.PI / 2)
          const y = 100 + 80 * Math.sin(i * angle - Math.PI / 2)
          return (
            <line
              key={`axis-${i}`}
              x1="100"
              y1="100"
              x2={x}
              y2={y}
              stroke="#475569"
              strokeWidth="0.5"
              opacity="0.6"
            />
          )
        })}

        {/* Data polygon with animation */}
        <polygon
          points={polygonPoints}
          fill="#3b82f6"
          fillOpacity="0.2"
          stroke="#3b82f6"
          strokeWidth="2"
          className="radar-path"
          style={{
            animation: animationComplete ? 'scaleIn 0.8s ease-out 0.2s forwards' : 'none',
          }}
        />

        {/* Data points */}
        {points.map((point, i) => (
          <circle
            key={`point-${i}`}
            cx={point[0]}
            cy={point[1]}
            r="3"
            fill="#3b82f6"
            style={{
              animation: `scaleIn 0.6s ease-out ${0.3 + i * 0.1}s forwards`,
              opacity: 0,
            }}
          />
        ))}

        {/* Labels */}
        {entries.map(([label, value], i) => {
          const x = 100 + 95 * Math.cos(i * angle - Math.PI / 2)
          const y = 100 + 95 * Math.sin(i * angle - Math.PI / 2)
          return (
            <text
              key={`label-${i}`}
              x={x}
              y={y}
              textAnchor="middle"
              dy="0.3em"
              fill="#d1d5db"
              fontSize="11"
              fontWeight="500"
              style={{
                animation: `slideUp 0.5s ease-out ${0.5 + i * 0.1}s forwards`,
                opacity: 0,
              }}
            >
              {label}
            </text>
          )
        })}
      </svg>
    </motion.div>
  )
}

// Animated Progress Bar with delayed animation
const AnimatedProgressBar = ({ label, value, color = 'bg-blue-500', delay = 0 }) => (
  <motion.div
    className="space-y-2 progress-bar-container"
    initial={{ opacity: 0, x: -20 }}
    animate={{ opacity: 1, x: 0 }}
    transition={{ duration: 0.5, delay }}
  >
    <div className="flex justify-between items-center">
      <span className="text-sm text-gray-400 font-medium">{label}</span>
      <span className="text-sm font-bold text-white">{value}%</span>
    </div>
    <div className="w-full h-3 bg-gray-700 rounded-full overflow-hidden border border-gray-600">
      <div
        className={`h-full ${color} rounded-full transition-all`}
        style={{
          width: 0,
          '--value': `${value}%`,
          animation: `fillProgress 1.2s cubic-bezier(0.34, 1.56, 0.64, 1) ${delay}s forwards`,
        }}
      />
    </div>
  </motion.div>
)

// Insight Card
const InsightCard = ({ icon, title, items, type = 'strength' }) => {
  const bgColor = type === 'strength'
    ? 'bg-green-500 bg-opacity-10 border-green-500'
    : 'bg-orange-500 bg-opacity-10 border-orange-500'
  const textColor = type === 'strength' ? 'text-green-400' : 'text-orange-400'

  return (
    <motion.div
      className={`${bgColor} border border-opacity-30 rounded-lg p-5 insight-card`}
      initial={{ opacity: 0, scale: 0.9 }}
      animate={{ opacity: 1, scale: 1 }}
      transition={{ duration: 0.5 }}
    >
      <div className={`flex items-center gap-2 mb-4 ${textColor}`}>
        <span className="text-2xl">{icon}</span>
        <h3 className="font-bold text-sm">{title}</h3>
      </div>
      <ul className="space-y-2">
        {items.map((item, i) => (
          <motion.li
            key={i}
            className="text-sm text-gray-300 flex gap-2"
            initial={{ opacity: 0, x: -10 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ delay: 0.1 * (i + 1) }}
          >
            <span className={`${textColor} font-bold`}>✓</span>
            <span>{item}</span>
          </motion.li>
        ))}
      </ul>
    </motion.div>
  )
}

// Progress Stepper
const ProgressStepper = ({ current = 1, total = 3 }) => {
  const steps = ['Beginner', 'Intermediate', 'Advanced']

  return (
    <motion.div
      className="space-y-6"
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      transition={{ duration: 0.6 }}
    >
      <div className="flex justify-between items-center">
        {steps.map((step, i) => (
          <div key={i} className="flex flex-col items-center flex-1">
            <motion.div
              className={`w-12 h-12 rounded-full flex items-center justify-center font-bold text-sm transition-all stepper-ball ${
                i < current
                  ? 'bg-green-500 text-white'
                  : i === current
                  ? 'bg-blue-500 text-white ring-4 ring-blue-400 ring-opacity-50'
                  : 'bg-gray-700 text-gray-400'
              }`}
              animate={i === current ? { scale: [1, 1.15, 1] } : {}}
              transition={{ duration: 2, repeat: Infinity }}
            >
              {i + 1}
            </motion.div>
            <p className="text-xs text-gray-400 mt-3 text-center">{step}</p>
          </div>
        ))}
      </div>

      {/* Progress Line */}
      <div className="flex gap-1 mt-2">
        {Array.from({ length: total }).map((_, i) => (
          <motion.div
            key={i}
            className={`h-1.5 flex-1 rounded-full transition-all ${
              i < current ? 'bg-green-500' : i === current ? 'bg-blue-500' : 'bg-gray-700'
            }`}
            initial={{ width: 0 }}
            animate={{ width: '100%' }}
            transition={{ delay: i * 0.2 }}
          />
        ))}
      </div>
    </motion.div>
  )
}

// Quick Action Card - WITH WORKING ONCLICK
const QuickActionCard = ({ icon, title, description, onClick }) => (
  <motion.button
    onClick={onClick}
    className="action-card text-left w-full group focus:outline-none"
    initial={{ opacity: 0, y: 20 }}
    animate={{ opacity: 1, y: 0 }}
    transition={{ duration: 0.5 }}
    whileHover={{ scale: 1.05 }}
    whileTap={{ scale: 0.95 }}
  >
    <div className="bg-gradient-to-br from-blue-600 to-blue-700 rounded-2xl p-6 transition-all">
      <div className="text-4xl mb-3">{icon}</div>
      <h3 className="font-bold text-white mb-2 text-lg">{title}</h3>
      <p className="text-sm text-blue-100 mb-4">{description}</p>
      <div className="flex items-center gap-2 text-sm text-blue-100 group-hover:translate-x-1 transition-transform duration-300">
        <span className="font-semibold">Get Started</span>
        <span>→</span>
      </div>
    </div>
  </motion.button>
)

export const Dashboard = ({ onNavigate = () => {} }) => {
  const { call } = useApi()
  const { token } = useAuth()
  const { autoAnalysis } = useResume()
  const [analysis, setAnalysis] = useState(null)

  useEffect(() => {
    if (autoAnalysis) {
      setAnalysis(autoAnalysis)
    } else if (token) {
      fetchLatestAnalysis()
    }
  }, [token, autoAnalysis])

  const fetchLatestAnalysis = async () => {
    try {
      const data = await call('GET', '/api/history')
      if (data && data.length > 0) {
        const latest = data[0]
        setAnalysis(latest.result)
      }
    } catch (err) {
      console.error('Error fetching analysis:', err)
    }
  }

  const score = analysis?.score || 7.5
  const strengths = analysis?.strengths || ['Clear structure', 'Good experience', 'Professional formatting']
  const weaknesses = analysis?.weaknesses || ['Limited metrics', 'Needs quantification', 'Missing keywords']
  const skillsMatched = analysis?.skills_matched || ['Python', 'Communication', 'Leadership']
  const skillsMissing = analysis?.skills_missing || ['Kubernetes', 'Advanced AWS']

  return (
    <>
      <style>{chartStyles}</style>
      <motion.div
        className="space-y-8"
        variants={pageVariants}
        initial="hidden"
        animate="visible"
      >
        {/* Hero Section - Gauge + Radar */}
        <motion.div
          variants={containerVariants}
          initial="hidden"
          animate="visible"
          className="grid grid-cols-1 md:grid-cols-3 gap-6"
        >
          {/* Gauge */}
          <motion.div variants={itemVariants} className="md:col-span-1">
            <div className="bg-gradient-to-br from-gray-900 to-gray-950 border border-gray-800 rounded-2xl p-8 backdrop-blur-xl">
              <h3 className="text-gray-300 text-sm font-medium text-center mb-6">Your Resume Strength</h3>
              <GaugeChart score={score} />
              <motion.p
                className="text-center mt-8 text-sm text-gray-400 font-medium"
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                transition={{ delay: 1.2 }}
              >
                {score >= 8 ? '🚀 Excellent!' : score >= 6 ? '👍 Good Job!' : '💪 Keep Improving!'}
              </motion.p>
            </div>
          </motion.div>

          {/* Radar Chart */}
          <motion.div variants={itemVariants} className="md:col-span-2">
            <div className="bg-gradient-to-br from-gray-900 to-gray-950 border border-gray-800 rounded-2xl p-8 backdrop-blur-xl">
              <h3 className="text-gray-300 text-sm font-medium mb-6">Skill Gap Analysis</h3>
              <SkillRadar
                skills={{
                  Python: skillsMatched.length > 0 ? 8 : 5,
                  SQL: skillsMatched.length > 1 ? 7 : 4,
                  ML: skillsMissing.includes('Machine Learning') ? 4 : 7,
                  Visualization: 6,
                  Communication: 8,
                }}
              />
            </div>
          </motion.div>
        </motion.div>

        {/* Stats Row */}
        <motion.div
          variants={containerVariants}
          initial="hidden"
          animate="visible"
          className="grid grid-cols-1 md:grid-cols-3 gap-4"
        >
          <motion.div variants={itemVariants}>
            <div className="stat-card bg-gradient-to-br from-green-500/20 to-green-600/20 border border-green-500/30 rounded-xl p-6 backdrop-blur-xl">
              <p className="text-green-400 text-sm mb-2 font-medium">Matched Skills</p>
              <p className="text-3xl font-bold text-white">{skillsMatched.length}</p>
            </div>
          </motion.div>

          <motion.div variants={itemVariants}>
            <div className="stat-card bg-gradient-to-br from-orange-500/20 to-orange-600/20 border border-orange-500/30 rounded-xl p-6 backdrop-blur-xl">
              <p className="text-orange-400 text-sm mb-2 font-medium">Skills to Learn</p>
              <p className="text-3xl font-bold text-white">{skillsMissing.length}</p>
            </div>
          </motion.div>

          <motion.div variants={itemVariants}>
            <div className="stat-card bg-gradient-to-br from-blue-500/20 to-blue-600/20 border border-blue-500/30 rounded-xl p-6 backdrop-blur-xl">
              <p className="text-blue-400 text-sm mb-2 font-medium">Overall Progress</p>
              <p className="text-3xl font-bold text-white">{Math.round((skillsMatched.length / (skillsMatched.length + skillsMissing.length)) * 100)}%</p>
            </div>
          </motion.div>
        </motion.div>

        {/* ATS Score Breakdown */}
        <motion.div
          variants={itemVariants}
          className="bg-gradient-to-br from-gray-900 to-gray-950 border border-gray-800 rounded-2xl p-8 backdrop-blur-xl"
        >
          <h3 className="text-white font-bold mb-8 text-lg">ATS Score Breakdown</h3>
          <div className="space-y-6">
            <AnimatedProgressBar label="Keyword Match" value={85} color="bg-green-500" delay={0.1} />
            <AnimatedProgressBar label="Formatting" value={78} color="bg-blue-500" delay={0.3} />
            <AnimatedProgressBar label="Impact & Achievements" value={72} color="bg-purple-500" delay={0.5} />
            <AnimatedProgressBar label="Readability" value={88} color="bg-cyan-500" delay={0.7} />
          </div>
        </motion.div>

        {/* Insights & Learning */}
        <motion.div
          variants={containerVariants}
          initial="hidden"
          animate="visible"
          className="grid grid-cols-1 md:grid-cols-2 gap-6"
        >
          {/* Insights */}
          <motion.div variants={itemVariants} className="space-y-4">
            <h3 className="text-white font-bold text-lg">Key Insights</h3>
            <InsightCard
              icon="✨"
              title="Top Strengths"
              items={strengths}
              type="strength"
            />
            <InsightCard
              icon="🎯"
              title="Areas to Improve"
              items={weaknesses}
              type="weakness"
            />
          </motion.div>

          {/* Learning Progress */}
          <motion.div variants={itemVariants}>
            <div className="bg-gradient-to-br from-gray-900 to-gray-950 border border-gray-800 rounded-2xl p-8 backdrop-blur-xl h-full">
              <h3 className="text-white font-bold mb-8 text-lg">Learning Progress</h3>
              <ProgressStepper current={2} total={3} />
            </div>
          </motion.div>
        </motion.div>

        {/* Quick Actions - WITH WORKING NAVIGATION */}
        <motion.div
          variants={containerVariants}
          initial="hidden"
          animate="visible"
        >
          <h3 className="text-white font-bold text-lg mb-4">Quick Actions</h3>
          <motion.div
            className="grid grid-cols-1 md:grid-cols-3 gap-4"
            variants={containerVariants}
          >
            <motion.div variants={itemVariants}>
              <QuickActionCard
                icon="📄"
                title="Analyze Resume"
                description="Get detailed insights and improvements"
                onClick={() => onNavigate('analyze')}
              />
            </motion.div>
            <motion.div variants={itemVariants}>
              <QuickActionCard
                icon="✍️"
                title="Improve Resume"
                description="Enhance your resume with AI suggestions"
                onClick={() => onNavigate('rewriter')}
              />
            </motion.div>
            <motion.div variants={itemVariants}>
              <QuickActionCard
                icon="📚"
                title="Generate Roadmap"
                description="Create your personalized learning path"
                onClick={() => onNavigate('learning')}
              />
            </motion.div>
          </motion.div>
        </motion.div>

        {/* Empty State */}
        {!analysis && (
          <motion.div
            className="bg-gradient-to-br from-blue-500/10 to-blue-600/10 border border-blue-500/30 rounded-2xl p-12 text-center backdrop-blur-xl"
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ delay: 0.5 }}
          >
            <p className="text-gray-400 mb-6 text-lg">📂 Upload your resume to see your personalized dashboard</p>
            <motion.button
              className="px-8 py-3 bg-blue-600 hover:bg-blue-700 rounded-lg text-white font-bold transition-all"
              whileHover={{ scale: 1.05 }}
              whileTap={{ scale: 0.95 }}
              onClick={() => onNavigate('resume')}
            >
              Upload Resume
            </motion.button>
          </motion.div>
        )}
      </motion.div>
    </>
  )
}
