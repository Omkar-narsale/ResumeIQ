import React, { useState, useEffect } from 'react'
import { motion } from 'framer-motion'
import { Card, CardTitle, CardContent } from '../components/Card'
import { useApi } from '../hooks/useApi'
import { pageVariants, containerVariants, itemVariants } from '../components/animations'

export const Achievements = () => {
  const [badges, setBadges] = useState(null)
  const [streak, setStreak] = useState(null)
  const [analysisCount, setAnalysisCount] = useState(0)
  const { call, loading } = useApi()

  useEffect(() => {
    loadData()
  }, [])

  const loadData = async () => {
    try {
      const badgesData = await call('GET', '/api/user-badges', null)
      const streakData = await call('GET', '/api/user-streak', null)
      setBadges(badgesData)
      setStreak(streakData)
    } catch (err) {
      console.error('Failed to load achievements:', err)
    }
  }

  const allBadges = [
    {
      id: 'first_analysis',
      name: '🎯 First Step',
      description: 'Completed your first resume analysis',
      icon: '🎯',
      progress: Math.min(analysisCount, 1)
    },
    {
      id: 'analyzer_pro',
      name: '📊 Analysis Pro',
      description: 'Completed 10 resume analyses',
      icon: '📊',
      progress: Math.min(analysisCount / 10, 1)
    },
    {
      id: 'streak_3',
      name: '🔥 On Fire',
      description: 'Maintained 3-day streak',
      icon: '🔥',
      progress: streak ? Math.min(streak.current_streak / 3, 1) : 0
    },
    {
      id: 'streak_7',
      name: '⚡ Week Warrior',
      description: 'Maintained 7-day streak',
      icon: '⚡',
      progress: streak ? Math.min(streak.current_streak / 7, 1) : 0
    },
    {
      id: 'feature_explorer',
      name: '🚀 Explorer',
      description: 'Used 5 different features',
      icon: '🚀',
      progress: 0.3
    },
    {
      id: 'all_features',
      name: '💎 Master',
      description: 'Used all major features',
      icon: '💎',
      progress: 0.5
    },
  ]

  const unlockedBadgeIds = badges?.badges.map(b => b.badge_name.split(' ')[0].toLowerCase()) || []

  return (
    <motion.div
      className="space-y-6"
      variants={pageVariants}
      initial="hidden"
      animate="visible"
    >
      {/* Streak Section */}
      <motion.div variants={itemVariants}>
        <Card>
          <CardTitle>🔥 Your Streak</CardTitle>
          <CardContent>
            <div className="grid grid-cols-3 gap-4">
              <div className="text-center">
                <div className="text-5xl font-bold text-red-400 mb-2">
                  {streak?.current_streak || 0}
                </div>
                <p className="text-gray-400 text-sm">Current Streak</p>
              </div>
              <div className="text-center">
                <div className="text-5xl font-bold text-orange-400 mb-2">
                  {streak?.longest_streak || 0}
                </div>
                <p className="text-gray-400 text-sm">Longest Streak</p>
              </div>
              <div className="text-center">
                <div className="text-5xl font-bold text-yellow-400 mb-2">
                  {streak?.total_activities || 0}
                </div>
                <p className="text-gray-400 text-sm">Total Activities</p>
              </div>
            </div>
          </CardContent>
        </Card>
      </motion.div>

      {/* Badges Grid */}
      <motion.div
        className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4"
        variants={containerVariants}
        initial="hidden"
        animate="visible"
      >
        {allBadges.map((badge) => {
          const isUnlocked = unlockedBadgeIds.includes(badge.id)

          return (
            <motion.div key={badge.id} variants={itemVariants}>
              <motion.div
                className={`p-4 rounded-lg border-2 transition-all h-full ${
                  isUnlocked
                    ? 'border-yellow-500 bg-yellow-500 bg-opacity-10 shadow-lg shadow-yellow-500/20'
                    : 'border-gray-700 bg-gray-800 bg-opacity-30'
                }`}
                whileHover={{ scale: isUnlocked ? 1.05 : 1 }}
              >
                <div className="text-center">
                  <div className={`text-6xl mb-2 ${isUnlocked ? '' : 'opacity-40'}`}>
                    {badge.icon}
                  </div>
                  <h3 className={`font-semibold mb-1 ${isUnlocked ? 'text-yellow-300' : 'text-gray-400'}`}>
                    {badge.name}
                  </h3>
                  <p className="text-xs text-gray-400 mb-3">{badge.description}</p>

                  {!isUnlocked && (
                    <div className="space-y-2">
                      <div className="w-full bg-gray-700 h-2 rounded-full overflow-hidden">
                        <motion.div
                          className="bg-gradient-to-r from-yellow-500 to-yellow-400 h-full"
                          initial={{ width: 0 }}
                          animate={{ width: `${badge.progress * 100}%` }}
                          transition={{ duration: 0.6 }}
                        />
                      </div>
                      <p className="text-xs text-gray-500">
                        {Math.round(badge.progress * 100)}% Complete
                      </p>
                    </div>
                  )}

                  {isUnlocked && (
                    <div className="text-yellow-300 text-sm font-semibold">
                      ✓ Unlocked
                    </div>
                  )}
                </div>
              </motion.div>
            </motion.div>
          )
        })}
      </motion.div>

      {/* Stats Section */}
      <motion.div variants={itemVariants}>
        <Card>
          <CardTitle>📊 Badge Stats</CardTitle>
          <CardContent>
            <div className="space-y-4">
              <div className="flex justify-between items-center">
                <span className="text-gray-400">Badges Unlocked</span>
                <span className="text-2xl font-bold text-yellow-400">
                  {badges?.total_badges || 0} / {allBadges.length}
                </span>
              </div>
              <div className="w-full bg-gray-700 h-3 rounded-full overflow-hidden">
                <motion.div
                  className="bg-gradient-to-r from-yellow-500 to-yellow-400 h-full"
                  initial={{ width: 0 }}
                  animate={{ width: `${((badges?.total_badges || 0) / allBadges.length) * 100}%` }}
                  transition={{ duration: 0.8 }}
                />
              </div>
              <p className="text-sm text-gray-400">
                Keep using features to unlock more badges and maintain your streak!
              </p>
            </div>
          </CardContent>
        </Card>
      </motion.div>

      {/* Tips Section */}
      <motion.div variants={itemVariants}>
        <Card>
          <CardTitle>💡 How to Earn Badges</CardTitle>
          <CardContent>
            <ul className="space-y-2 text-sm text-gray-300">
              <li>✓ <strong>First Step:</strong> Complete your first resume analysis</li>
              <li>✓ <strong>Analysis Pro:</strong> Analyze 10 resumes</li>
              <li>✓ <strong>On Fire:</strong> Use the app for 3 consecutive days</li>
              <li>✓ <strong>Week Warrior:</strong> Use the app for 7 consecutive days</li>
              <li>✓ <strong>Explorer:</strong> Try 5 different features</li>
              <li>✓ <strong>Master:</strong> Use all major features</li>
            </ul>
          </CardContent>
        </Card>
      </motion.div>
    </motion.div>
  )
}
